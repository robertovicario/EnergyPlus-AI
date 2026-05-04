FROM python:3.9-slim

WORKDIR /app

COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ .
COPY data/config/ ./data/config/
COPY data/templates/ ./data/templates/
COPY data/udse.parquet ./data/udse.parquet
COPY models/ ./models/

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
