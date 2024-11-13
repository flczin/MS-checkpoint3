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
def generate_diploma(data: Diploma):
    key = str(uuid.uuid3(uuid.NAMESPACE_DNS, f"{data.nome}{data.curso}"))
    app_dir = os.getcwd()
    path = os.path.join(app_dir, f"diplomas/{key}.pdf")
    data.path = path   
    data.key = key
    print(key)
    task = celery_worker.send_task("generate_diploma", args=[data.model_dump()], task_id=key)
    
    return {"key": task.id}
    
        
@app.get("/retrieve_diploma/{uuid}")
def retrieve_diploma(uuid, collection=Depends(get_collection)):
    possible = cache.get(uuid)
    if possible:
        print("cache")
        return FileResponse(path=possible, media_type='application/pdf',
                        status_code=200, content_disposition_type="attachment", filename=f"{uuid}.pdf")
    
    db = collection.find_one({"key": uuid})
    if db:
        cache.set(uuid, db["path"], ex=60)
        print("db")
        return FileResponse(path=db["path"], media_type='application/pdf',
                status_code=200, content_disposition_type="attachment", filename=f"{uuid}.pdf") 
    
    result = AsyncResult(id=uuid, app=celery_worker)
    if result.state != "SUCCESS":
        return {"File still being processed or do not exist"}
    else:
        return FileResponse(path=result.result["path"], media_type='application/pdf',
                        status_code=200, content_disposition_type="attachment", filename=f"{uuid}.pdf")


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)