FROM python:3.9-slim

LABEL maintainer="Alexander Ivanov <oz.sasha.ivanov@gmail.com>"

# System envoriments
ENV LANG=C.UTF-8 \
  PYTHONUNBUFFERED=1

WORKDIR /app

# Project's web server
RUN pip install gunicorn

# Project's requirements
COPY requirements.txt .
RUN pip install -r requirements.txt

# Target project
COPY . .

EXPOSE 8000

CMD gunicorn notes.wsgi -w 4 -t 600 -b 0.0.0.0:8000
