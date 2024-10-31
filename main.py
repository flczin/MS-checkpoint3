from fastapi import FastAPI, Depends
from fastapi.responses import FileResponse
from model import Diploma
import uvicorn
from pymongo import MongoClient
import redis
import uuid
from worker import celery_worker
from celery.result import AsyncResult
import os


app = FastAPI()
cache = redis.Redis.from_url("redis://redis:6379/0")

def get_collection():
    client = MongoClient("mongodb://mongodb:27017/")
    return client.instituto.diplomas


@app.post("/generate_diploma")
def generate_diploma(data: Diploma, collection=Depends(get_collection)):
    key = str(uuid.uuid3(uuid.NAMESPACE_DNS, f"{data.nome_aluno}{data.curso}"))
    app_dir = os.getcwd()
    path = os.path.join(app_dir, f"diplomas/{key}.pdf")
    data.path = path   
    possible = cache.get(key)
    if possible:
        print("cache")
        return FileResponse(path=possible, media_type='application/pdf',
                        status_code=200, content_disposition_type="attachment", filename=f"{key}.pdf")
    else:
        db = collection.find_one({"path": data.path})
        if db:
            cache.set(key, path, ex=60)
            print("db")
            return FileResponse(path=db["path"], media_type='application/pdf',
                        status_code=200, content_disposition_type="attachment", filename=f"{key}.pdf")
        else:
            task = celery_worker.send_task("generate_diploma", args=[data.model_dump()])
            task_result = AsyncResult(id=task.id, app=celery_worker).get()
            collection.insert_one(data.model_dump())
            print("worker")
            return FileResponse(path=task_result["path"], media_type='application/pdf',
                        status_code=200, content_disposition_type="attachment", filename=f"{key}.pdf")
        

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)