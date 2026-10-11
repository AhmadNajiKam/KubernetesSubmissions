FROM python:3.12-slim

WORKDIR /app

RUN pip install --no-cache-dir fastapi uvicorn

COPY main.py .

RUN mkdir -p /app/shared

EXPOSE 4000

CMD ["python", "main.py"]
