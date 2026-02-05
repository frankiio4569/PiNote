from flask import Flask, render_template, redirect, url_for, request, flash, session
from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timezone
import os

app = Flask(__name__)

APP_VERSION = "2.2.2"

@app.context_processor
def inject_version():
    return dict(version=APP_VERSION)

app.config['SECRET_KEY'] = 'chiave-segreta-molto-difficile-cambiala'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///notes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# --- MODELLI ---

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    content = db.Column(db.Text, nullable=False)
    date_updated = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    is_protected = db.Column(db.Boolean, default=False)
    protection_password = db.Column(db.String(150), nullable=True)
    # NUOVO CAMPO PER IL CESTINO
    is_deleted = db.Column(db.Boolean, default=False)

class NoteVersion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    note_id = db.Column(db.Integer, db.ForeignKey('note.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    date_archived = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

# --- ROUTE ---

@app.route('/')
@login_required
def index():
    # Mostra solo le note NON cancellate (is_deleted=False)
    user_notes = Note.query.filter_by(user_id=current_user.id, is_deleted=False).order_by(Note.date_updated.desc()).all()
    return render_template('index.html', notes=user_notes)

@app.route('/trash')
@login_required
def trash():
    # Mostra solo le note NEL CESTINO (is_deleted=True)
    trash_notes = Note.query.filter_by(user_id=current_user.id, is_deleted=True).order_by(Note.date_updated.desc()).all()
    return render_template('trash.html', notes=trash_notes)

@app.route('/note/new', methods=['GET', 'POST'])
@login_required
def new_note():
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        is_prot = request.form.get('is_protected') == 'on'
        prot_pass = request.form.get('protection_password')
        hashed_prot_pass = generate_password_hash(prot_pass) if is_prot and prot_pass else None

        new_note = Note(title=title, content=content, user_id=current_user.id, 
                        is_protected=is_prot, protection_password=hashed_prot_pass)
        db.session.add(new_note)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('editor.html', note=None)

@app.route('/note/unlock/<int:id>', methods=['GET', 'POST'])
@login_required
def unlock_note(id):
    note = db.session.get(Note, id)
    
    # Controlli di sicurezza base
    if not note or note.user_id != current_user.id or note.is_deleted:
        return "Accesso negato", 403
    
    # Se la nota non è protetta, non serve sbloccarla
    if not note.is_protected:
        return redirect(url_for('edit_note', id=id))

    if request.method == 'POST':
        password_attempt = request.form.get('password')
        # Verifica se la password è corretta
        if note.protection_password and check_password_hash(note.protection_password, password_attempt):
            # SALVA NELLA SESSIONE CHE QUESTA NOTA È APERTA
            session[f'unlocked_{id}'] = True
            return redirect(url_for('edit_note', id=id))
        else:
            flash('Password errata!')
            
    return render_template('unlock.html', note=note)

@app.route('/note/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_note(id):
    note = db.session.get(Note, id)
    # Non permettere modifica se è nel cestino o non è tua
    if not note or note.user_id != current_user.id or note.is_deleted:
        return "Accesso negato", 403
# --- CONTROLLO PASSWORD ---
    if note.is_protected and not session.get(f'unlocked_{id}'):
        return redirect(url_for('unlock_note', id=id))
    # --------------------------
    if request.method == 'POST':
        version = NoteVersion(note_id=note.id, content=note.content)
        db.session.add(version)
        
        note.title = request.form.get('title')
        note.content = request.form.get('content')
        note.date_updated = datetime.now(timezone.utc)
        db.session.commit()
        flash('Nota aggiornata!')
        return redirect(url_for('index'))
    
    return render_template('editor.html', note=note)

# --- NUOVE FUNZIONI CESTINO ---

@app.route('/note/move_to_trash/<int:id>')
@login_required
def move_to_trash(id):
    note = db.session.get(Note, id)
    if note and note.user_id == current_user.id:
        note.is_deleted = True
        db.session.commit()
        flash('Nota spostata nel cestino.')
    return redirect(url_for('index'))

@app.route('/note/restore/<int:id>')
@login_required
def restore_note(id):
    note = db.session.get(Note, id)
    if note and note.user_id == current_user.id:
        note.is_deleted = False
        db.session.commit()
        flash('Nota ripristinata!')
    return redirect(url_for('trash'))

@app.route('/note/delete_forever/<int:id>')
@login_required
def delete_forever(id):
    note = db.session.get(Note, id)
    if note and note.user_id == current_user.id:
        # Elimina anche le versioni storiche collegate per pulizia
        NoteVersion.query.filter_by(note_id=id).delete()
        db.session.delete(note)
        db.session.commit()
        flash('Nota eliminata definitivamente.')
    return redirect(url_for('trash'))

# --- FINE NUOVE FUNZIONI ---

@app.route('/note/versions/<int:id>')
@login_required
def versions(id):
    note = db.session.get(Note, id)
    if not note or note.user_id != current_user.id: return "Accesso negato", 403
    
# --- CONTROLLO PASSWORD ---
    if note.is_protected and not session.get(f'unlocked_{id}'):
        flash("Sblocca la nota per vedere la cronologia.")
        return redirect(url_for('unlock_note', id=id))
    # --------------------------

    history = NoteVersion.query.filter_by(note_id=id).order_by(NoteVersion.date_archived.desc()).all()
    return render_template('versions.html', note=note, history=history)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('index'))
        flash('Credenziali errate')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if User.query.filter_by(username=username).first():
            flash('Utente esistente')
            return redirect(url_for('register'))
        new_user = User(username=username, password=generate_password_hash(password))
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect(url_for('index'))
    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5001, debug=True)
