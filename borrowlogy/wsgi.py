"""
WSGI config for borrowlogy project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""

import os
import sys
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

try:
    logger.info("Starting WSGI application loading...")
    logger.info(f"Current Python path: {sys.path}")

    from django.core.wsgi import get_wsgi_application

    logger.info(f"DJANGO_SETTINGS_MODULE before setdefault: {os.environ.get('DJANGO_SETTINGS_MODULE')}")
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'borrowlogy.settings_prod')
    logger.info(f"DJANGO_SETTINGS_MODULE after setdefault: {os.environ.get('DJANGO_SETTINGS_MODULE')}")

    logger.info("Getting WSGI application...")
    application = get_wsgi_application()
    logger.info("WSGI application loaded successfully.")

except Exception as e:
    logger.error(f"Failed to load WSGI application: {str(e)}", exc_info=True)
    raise