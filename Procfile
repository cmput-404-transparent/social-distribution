web: cd frontend && npm run build && cd .. && cd backend && python manage.py collectstatic --noinput && python manage.py migrate && gunicorn backend.wsgi --log-file -
