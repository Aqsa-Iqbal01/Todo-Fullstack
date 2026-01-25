FROM python:3.11-slim


WORKDIR /app

# Install PostgreSQL development headers and other dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    postgresql-contrib \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Expose the port
EXPOSE 7860

# Set the command to run the application
CMD ["sh", "-c", "uvicorn src.main:app --host 0.0.0.0 --port ${PORT:-7860}"]