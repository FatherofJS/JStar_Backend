FROM python:3.12-slim

# Install system dependencies for astrology libraries (swisseph)
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    make \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Add a non-root user for security
RUN useradd -m jstar && chown -R jstar /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Switch to the non-root user
USER jstar

# Use uvicorn as the process manager
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"]
