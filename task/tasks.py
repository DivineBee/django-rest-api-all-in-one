from djangoProject.celery import app

@app.task
def send_something():
    print("Hellloooo from le Celery")

