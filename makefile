# Makefile per il progetto

.PHONY: install run clean docker_build docker_run

# Installazione delle dipendenze
install:
    pip install -r requirements.txt

# Esecuzione del progetto
run:
    python ai_ntavola.py

# Pulizia della cartella di output
clean:
    rm -rf ricette_db

# Build del Docker container
docker_build:
    docker build -t ricette-app .

# Esecuzione del Docker container
docker_run:
    docker run -p 11434:11434 ricette-app
