# Usa un'immagine di base Python
FROM python:3.11 or above 

# Imposta la directory di lavoro
WORKDIR /app

# Copia i file del progetto nel container
COPY . /app

# Installa le dipendenze
RUN pip install --no-cache-dir -r requirements.txt

# Esponi la porta su cui il server LLM è in esecuzione
EXPOSE 11434

# Comando per eseguire il progetto
CMD ["python", "ai_ntavola.py"]
