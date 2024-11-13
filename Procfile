web: gunicorn backend.wsgi --chdir backend

release: python manage.py migrate
web: gunicorn backend.wsgi --chdir backend --log-file -