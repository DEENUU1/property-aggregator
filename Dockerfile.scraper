FROM python:3.12

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc

COPY requirements.txt .
COPY .env /app/.env

RUN pip install -r requirements.txt

RUN addgroup --system app && adduser --system --group app

COPY ./scraper /app

ENTRYPOINT ["python", "main.py"]
