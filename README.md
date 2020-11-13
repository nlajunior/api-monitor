# api-monitor
python -m pip install --user virtualenv

# Testando Gunicorn
gunicorn --bind 0.0.0.0:8080 wsgi:app