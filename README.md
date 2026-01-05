# Progetto Ricette

Questo progetto permette di generare ricette personalizzate a partire da un dataset JSON di ricette, utilizzando modelli di deep learning e un database vettoriale per il recupero delle informazioni.

## Requisiti

- Python 3.11
- Docker (opzionale)

## Installazione

1. Clona il repository:
    ```bash
    git clone https://github.com/Christianwork-hub/AI_ntavola.git
    cd ricette
    ```

2. Installa le dipendenze:
    ```bash
    make install
    ```

3. Avvia il progetto:
    ```bash
    make run
    ```

## Uso

Una volta avviato il progetto, puoi porre domande riguardo le ricette, come:

- "Generami una ricetta con parmigiano, melanzane e pomodoro"

Il sistema restituirà una ricetta basata sul dataset e sui modelli configurati.

## Docker

Puoi anche eseguire il progetto in un container Docker:

1. Costruisci l'immagine Docker:
    ```bash
    make docker_build
    ```

2. Avvia il container:
    ```bash
    make docker_run
    ```

## Licenza

Questo progetto è distribuito sotto la licenza MIT.
