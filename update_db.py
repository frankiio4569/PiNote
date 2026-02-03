import sqlite3

# Connettiti al database
conn = sqlite3.connect('notes.db')
cursor = conn.cursor()

try:
    # Aggiunge la colonna is_deleted (booleano, default 0 cioè Falso)
    cursor.execute("ALTER TABLE note ADD COLUMN is_deleted BOOLEAN DEFAULT 0")
    print("Database aggiornato con successo! Colonna 'is_deleted' aggiunta.")
except sqlite3.OperationalError:
    print("La colonna esiste già o errore nel database.")

conn.commit()
conn.close()
