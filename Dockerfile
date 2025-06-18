FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV FLASK_APP=main.py
ENV FLASK_ENV=development

# Set work directory
WORKDIR /app

# Install system dependencies including those needed for ML libraries
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    curl \
    wget \
    git \
    build-essential \
    python3-dev \
    libffi-dev \
    libssl-dev \
    libblas-dev \
    liblapack-dev \
    libatlas-base-dev \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies with specific versions for compatibility
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir wheel setuptools
RUN pip install --no-cache-dir -r requirements.txt

# Download NLTK data
RUN python -c "import nltk; nltk.download('punkt', quiet=True); nltk.download('stopwords', quiet=True); print('NLTK data downloaded')" || echo "NLTK download failed, continuing..."

# Copy project files
COPY . .

# Create necessary directories
RUN mkdir -p uploads logs embeddings
RUN chmod 755 uploads logs embeddings

# Copy model files if they exist
RUN if [ -f "app/model/siamese_model.h5" ]; then echo "Model file found"; else echo "Model file not found, creating placeholder"; mkdir -p app/model; fi

# Change ownership to appuser
RUN chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Expose port
EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:5000/health || exit 1

# Run the application
CMD ["python", "main.py"]