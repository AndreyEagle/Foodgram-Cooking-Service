FROM python:3.7-slim

COPY /backend /app

RUN pip install --upgrade pip

RUN pip install -r app/requirements.txt --no-cache-dir

WORKDIR /app

CMD ["gunicorn", "backend.wsgi:application", "--bind", "0:8000" ]