FROM python:latest

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY scheduler.py .
COPY scraper_v1.py .

CMD ["sh", "-c", "python scheduler.py && sleep infinity"]
