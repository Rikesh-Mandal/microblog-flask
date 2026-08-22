FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir gunicorn pymysql


COPY app app
COPY migrations migrations
COPY microblog.py config.py boot.sh ./

RUN chmod a+x boot.sh

ENV FLASK_APP=microblog.py

RUN mkdir -p db

RUN flask translate compile

EXPOSE 8000
ENTRYPOINT ["./boot.sh"]