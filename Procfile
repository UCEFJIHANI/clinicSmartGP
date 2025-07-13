web: python manage.py migrate && mkdir -p staticfiles && python manage.py collectstatic --noinput && gunicorn clinicSmart.wsgi --bind 0.0.0.0:$PORT --workers 2 --timeout 120 --access-logfile -
