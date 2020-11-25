import multiprocessing

cores = multiprocessing.cpu_count()

# Gunicorn config variables
loglevel = "info"
workers = 2 * cores + 1
bind = "0.0.0.0:8000"
errorlog = "/logs/gunicorn_errors.log"
worker_tmp_dir = "/dev/shm"
accesslog = "/logs/gunicorn_access.log"
graceful_timeout = 120
timeout = 120
keepalive = 5
