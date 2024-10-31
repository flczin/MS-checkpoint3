from fastapi import FastAPI, Depends
from fastapi.responses import JSONResponse
from model import Diploma
import uvicorn
from pymongo import MongoClient
import redis
import uuid
import os

app = FastAPI()
cache = redis.Redis.from_url("redis://localhost:6379/0")

def get_collection():
    client = MongoClient("mongodb://localhost:27017/")
    return client.instituto.diplomas


@app.post("/generate_diploma")
def generate_diploma(data: Diploma, collection=Depends(get_collection)):
    key = str(uuid.uuid3(uuid.NAMESPACE_DNS, f"{data.nome_aluno}{data.curso}"))
    path = f"{key}.pdf"
    data.path = path
    possible = cache.get(key)
    if possible:
        return JSONResponse(status_code=200, content={"path": str(possible), "from": "cache"})
    else:
        db = collection.find_one({"path": data.path})
        if db:
            cache.set(key, path, ex=10)
            return JSONResponse(status_code=200, content={"path": db["path"], "from": "db"})
        else:
            collection.insert_one(data.model_dump())
        
            return JSONResponse(status_code=201, content={"path": path, "from": None})


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)