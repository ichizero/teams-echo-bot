FROM python:3.7-slim

WORKDIR /bot-app
COPY requirements.txt .

RUN pip install --no-cache -r requirements.txt && \
    rm requirements.txt

ENTRYPOINT gunicorn -b :5555 app:app
