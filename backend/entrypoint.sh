python manage.py migrate
python manage.py collectposts
gunicorn --bind=0.0.0.0:8080 --workers=2 backend.wsgi:application