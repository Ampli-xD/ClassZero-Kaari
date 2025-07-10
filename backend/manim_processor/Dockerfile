FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    texlive-full \
    build-essential \
    cmake \
    ffmpeg \
    git \
    libcairo2-dev \
    libffi-dev \
    libpango1.0-dev \
    pkg-config \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application
COPY manim_processor.py .

# Create directories for outputs and temp files
RUN mkdir -p /app/outputs /app/temp

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV MANIM_CACHE_DIR=/app/cache
ENV MANIM_MAX_WORKERS=4

# Run the application
CMD ["python", "manim_processor.py"]