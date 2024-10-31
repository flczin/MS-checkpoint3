from celery import Celery
from jinja2 import FileSystemLoader, Environment
from xhtml2pdf import pisa

config = {
    "mongodb_scheduler_db": "worker_diplomas",
    "mongodb_scheduler_url": "mongodb://mongodb:27017/"
}
celery_worker = Celery("worker", broker="mongodb://mongodb:27017/queue_diplomas", backend="mongodb://mongodb:27017/queue_diplomas")
celery_worker.conf.update(**config)

env = Environment(loader=FileSystemLoader("."))
template = env.get_template("./templates/template.html")

@celery_worker.task(name="generate_diploma")
def generate_diploma(data):
    try:
        populated = template.render(data)
        with open(data["path"], "w+b") as output_file:
            pisa.CreatePDF(populated, dest=output_file)
        return {"from": "worker", "path": data["path"]}
    except Exception as e:
        return str(e)
