FROM python:3.11-slim
#ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
RUN apt-get update
RUN apt-get install -y cron
WORKDIR /code
COPY requirements.txt /code/
RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt
COPY . /code/

ENTRYPOINT ["bash", "docker-entrypoint.sh"]

EXPOSE 8000

# worker should be according to the CFN config
# --workers=WORKERS, The number of worker processes. This number should generally be between 2-4 workers per core in the server.
# Gunicorn relies on the operating system to provide all of the load balancing when handling requests. Generally they recommend (2 x $num_cores) + 1 as the number of workers to start off with.
CMD ["gunicorn", "--workers=3", "--timeout=120", "--worker-class=gevent", "--bind 0.0.0.0:8000", "teamfriends.wsgi"]