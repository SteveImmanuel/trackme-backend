FROM python:3.8

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY trackme /app/trackme
COPY requirements.txt /app

WORKDIR /app
RUN pip install -r requirements.txt

EXPOSE 5000
CMD gunicorn --workers 3 --bind 0.0.0.0:5000 trackme.wsgi:app