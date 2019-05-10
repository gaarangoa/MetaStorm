echo Starting Gunicorn.
exec gunicorn admin.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 3