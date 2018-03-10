FROM python

WORKDIR /usr/share/backend
ADD . .
RUN pip install -r requirements.txt

EXPOSE 8080

# CMD ["python", "manage.py", "runserver", "0.0.0.0:8080"]
CMD ["gunicorn", "--bind=0.0.0.0:8080", "--workers=2", "backend.wsgi:application"]