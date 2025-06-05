bind = "0.0.0.0:8000"
workers = 1
worker_class = "sync"
timeout = 30
threads = 1

#gunicorn exchangerate.asgi:application -c gunicorn.conf.py
#gunicorn currency.wsgi:application -c gunicorn.conf.py

