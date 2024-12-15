import os
from django.core.wsgi import get_wsgi_application

# Set the default settings module for the 'conf' project.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'conf.settings')

# Get the WSGI application.
application = get_wsgi_application()

# Import and use Waitress to serve the application if needed directly.
if __name__ == "__main__":
    from waitress import serve

    serve(application, host='0.0.0.0', port=8000)
