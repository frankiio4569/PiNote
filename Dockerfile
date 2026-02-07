# Usa Python leggero
FROM python:3.11-slim

# Imposta la cartella di lavoro
WORKDIR /app

# Installa strumenti di sistema necessari
RUN apt-get update && apt-get install -y gcc && rm -rf /var/lib/apt/lists/*

# Copia i requisiti e installa le librerie
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia tutto il resto del codice
COPY . .

# Crea la cartella per i dati
RUN mkdir -p /app/data

# Porta su cui gira l'app
EXPOSE 5001

# Comando di avvio
CMD ["python", "app.py"]
