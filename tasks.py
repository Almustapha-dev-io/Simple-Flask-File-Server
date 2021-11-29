import os
from celery import Celery

client = Celery("tasks", broker=os.environ.get("BROKER_URL", "redis://localhost:6379/0"),
                backend=os.environ.get("BACKEND_URL", "redis://localhost:6379/1"))


@client.task
def save_file(file, dir):
    print(file)
    file.save(dir)
