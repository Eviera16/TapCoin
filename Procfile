release: python manage.py makemigrations --no-input
release: python manage.py migrate --no-input
web: gunicorn TCServer.wsgi
celery: celery -A TCServer.celery worker -l info
celerybeat: celery -A TCServer beat -l INFO