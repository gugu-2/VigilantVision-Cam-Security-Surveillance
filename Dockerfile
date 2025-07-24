# Base image
FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y     ffmpeg     libgl1-mesa-glx     && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY backend ./backend
COPY frontend ./frontend
COPY models ./models

# Expose port
EXPOSE 5000

# Set working directory to backend and start app
WORKDIR /app/backend
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]