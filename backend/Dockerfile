FROM python:3.11-slim

WORKDIR /app

COPY ./requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY ./ ./

CMD ["sh", "-c", "python3 ./CineBrain/manage.py makemigrations movies && python3 ./CineBrain/manage.py migrate && python3 ./CineBrain/manage.py runserver 0.0.0.0:8000"]
