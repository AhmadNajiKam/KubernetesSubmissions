FROM python:3.11-slim AS base
WORKDIR /app

FROM base AS generator

COPY generator.py .

CMD ["python",  "generator.py"]

FROM base AS server

COPY server.py .

RUN pip install --no-cache-dir fastapi uvicorn

CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "5000"]
