import multiprocessing

# https://docs.gunicorn.org/en/stable/configure.html#configuration-file

wsgi_app = "movieclub.wsgi"

accesslog = "-"

workers = multiprocessing.cpu_count() * 2 + 1
