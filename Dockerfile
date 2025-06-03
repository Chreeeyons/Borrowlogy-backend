FROM python:3.12-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Set environment variables
ENV DJANGO_SETTINGS_MODULE=borrowlogy.settings_prod
ENV PYTHONUNBUFFERED=1
ENV PORT=8000
ENV DJANGO_ALLOWED_HOSTS=*

# Create necessary directories and ensure migrations exist
RUN mkdir -p /app/staticfiles
RUN mkdir -p /app/authentication/migrations
RUN touch /app/authentication/migrations/__init__.py

# Create a script to handle migrations and startup
RUN echo '#!/bin/bash\n\
python manage.py makemigrations authentication --noinput\n\
python manage.py migrate --noinput\n\
python manage.py collectstatic --noinput\n\
exec gunicorn borrowlogy.wsgi:application --bind 0.0.0.0:${PORT:-8000} --workers 4 --timeout 300 --log-level info --access-logfile - --error-logfile - --capture-output --preload\n\
' > /app/start.sh && chmod +x /app/start.sh

# Expose the port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=30s --retries=3 \
    CMD curl -f http://localhost:8000/ || exit 1

# Use the startup script
CMD ["/app/start.sh"]