FROM python:3.8-slim AS builder

WORKDIR /app

COPY ./app/requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r requirements.txt

FROM python:3.8-slim

WORKDIR /app

COPY --from=builder /usr/local/lib/python3.8/site-packages /usr/local/lib/python3.8/site-packages

COPY ./app /app
COPY start.sh /start.sh

RUN chmod +x /start.sh

CMD ["/start.sh"]
