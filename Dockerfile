FROM python:3.11-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# System deps (pdfplumber)
RUN apt-get update && apt-get install -y \
    poppler-utils \
    && rm -rf /var/lib/apt/lists/*

# Copy only requirements first (better caching)
COPY backend/requirements.txt ./requirements.txt

# Install Python deps
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy backend source
COPY backend/ .

# Cloud Run port
EXPOSE 8080

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]