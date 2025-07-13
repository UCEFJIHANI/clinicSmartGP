web: python manage.py migrate && python manage.py check --deploy && gunicorn clinicSmart.wsgi --bind 0.0.0.0:$PORT --workers 2 --timeout 120
