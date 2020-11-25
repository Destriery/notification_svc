# образ для установки зависимостей из requirements.txt
FROM    python:3.8 as builder

COPY    requirements.txt .

RUN     python -m venv .venv &&\
        . .venv/bin/activate &&\
        pip install --upgrade pip &&\
        pip install --no-cache-dir uvicorn gunicorn &&\
        pip install --no-cache-dir -r requirements.txt

# базовый образ
FROM    python:3.8-slim

ENV     LANG C.UTF-8
ENV     TZ Europe/Moskow

ENV     PROJECTPATH /app
ENV     PYTHONPATH /.venv

WORKDIR ${PROJECTPATH}

RUN     mkdir .venv
RUN     mkdir .temp
RUN     mkdir /logs

COPY    ./gunicorn.conf.py /gunicorn.conf.py
COPY    --from=builder /${PYTHONPATH} /${PYTHONPATH} 
COPY    . .

EXPOSE  8000

CMD     [ "/.venv/bin/gunicorn", "--worker-class=uvicorn.workers.UvicornH11Worker", "--config=gunicorn.conf.py", "main:application" ]