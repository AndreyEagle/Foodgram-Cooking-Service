FROM python:3.7-slim

COPY /backend /app

RUN pip install --upgrade pip

WORKDIR /app

RUN pip install -r requirements.txt --no-cache-dir

CMD ["gunicorn", "backend.wsgi:application", "--bind", "0:8000" ]