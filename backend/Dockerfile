FROM python:3.7-slim

WORKDIR /app

COPY /api_foodgram /app

RUN pip install --upgrade pip

RUN pip install -r app/requirements.txt

CMD ["gunicorn", "api_foodgram.wsgi:application", "--bind", "0:8000" ]