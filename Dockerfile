FROM python:3.8-slim

WORKDIR /app

COPY ./app/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

RUN pip install nltk && \
    python -m nltk.downloader vader_lexicon

RUN python -m spacy download en_core_web_sm
RUN python -m spacy download it_core_news_md


COPY ./app /app
COPY start.sh /start.sh

RUN chmod +x /start.sh

CMD ["/start.sh"]
