import os
import sys

try:
    print("Attempting to set DJANGO_SETTINGS_MODULE...")
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'borrowlogy.settings_prod')
    print(f"DJANGO_SETTINGS_MODULE set to: {os.environ.get('DJANGO_SETTINGS_MODULE')}")

    print("Attempting to import Django settings...")
    from django.conf import settings
    settings.configure()
    print("Django settings imported successfully.")

    print("Attempting to import WSGI application...")
    from borrowlogy.wsgi import application
    print("WSGI application imported successfully.")

    print("Startup check complete - success!")
    sys.exit(0)

except Exception as e:
    print(f"Startup check failed: {e}", file=sys.stderr)
    sys.exit(1) 