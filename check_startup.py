import os
import sys
import logging
import django
from django.db import connection

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

def check_database():
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        logger.info("Database connection successful")
        return True
    except Exception as e:
        logger.error(f"Database connection failed: {str(e)}")
        return False

def main():
    try:
        logger.info("Starting application health check...")
        
        # Set Django settings module
        logger.info("Setting DJANGO_SETTINGS_MODULE...")
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'borrowlogy.settings_prod')
        logger.info(f"DJANGO_SETTINGS_MODULE set to: {os.environ.get('DJANGO_SETTINGS_MODULE')}")

        # Initialize Django
        logger.info("Initializing Django...")
        django.setup()
        logger.info("Django initialized successfully")

        # Check database connection
        logger.info("Checking database connection...")
        if not check_database():
            logger.error("Database check failed")
            sys.exit(1)

        # Import WSGI application
        logger.info("Importing WSGI application...")
        from borrowlogy.wsgi import application
        logger.info("WSGI application imported successfully")

        logger.info("Health check completed successfully!")
        sys.exit(0)

    except Exception as e:
        logger.error(f"Health check failed: {str(e)}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    main() 