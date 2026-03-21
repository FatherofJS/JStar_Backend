FROM python:3.12-slim

# Install the exact C++ underlying compilers required for astrology charting
RUN apt-get update && apt-get install -y gcc g++ make

WORKDIR /app

# Install pip requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all the actual project code into the container
COPY . .

# Finally, execute FastAPI exactly as your Procfile directed
CMD uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}
