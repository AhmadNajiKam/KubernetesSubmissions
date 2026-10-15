FROM python:3.12-slim

WORKDIR /app

COPY main.py .

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

RUN mkdir -p /app/shared

EXPOSE 4000

CMD ["python", "main.py"]
