# Use Python 3.11 slim image as base
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy application files
COPY app.py create_db.py ./
COPY templates/ ./templates/

# Install Python dependencies
RUN pip install --no-cache-dir \
    Flask==2.3.0 \
    APScheduler==3.10.4

# Initialize database on startup
RUN python create_db.py

# Expose port
EXPOSE 5000

# Set environment variables
ENV FLASK_APP=app.py

# Run the application
CMD ["python", "-m", "flask", "run", "--host=0.0.0.0"]
