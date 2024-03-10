# Usa un'immagine Python ufficiale come immagine di base
FROM python:3.8-slim

# Imposta la directory di lavoro nel container
WORKDIR /app

# Copia i file dei requisiti e installa le dipendenze
COPY ./app/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

# Copia il resto del codice sorgente dell'applicazione e lo script di avvio
COPY ./app /app
COPY start.sh /start.sh

# Assicurati che lo script di avvio sia eseguibile
RUN chmod +x /start.sh

# Usa lo script di avvio come comando di avvio del container
CMD ["/start.sh"]
