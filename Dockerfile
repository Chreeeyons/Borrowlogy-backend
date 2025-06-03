FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV DJANGO_SETTINGS_MODULE=borrowlogy.settings_prod

# Collect static files
RUN python manage.py collectstatic --noinput

# Command to run the application using Gunicorn
CMD ["gunicorn", "borrowlogy.wsgi:application", "--bind", "0.0.0.0:$PORT"] 