FROM python:3.11-slim

WORKDIR /app

COPY ./requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt
COPY --chmod=777 ./CineBrain/create_superuser.py /backend/data/create_superuser.py
# RUN chmod +x /app/CineBrain

COPY ./ ./

CMD ["sh", "-c", "python3 ./CineBrain/manage.py makemigrations  && python3 ./CineBrain/manage.py migrate &&  python ./CineBrain/create_superuser.py && python3 ./CineBrain/manage.py runserver 0.0.0.0:8000"]
