from contextlib import asynccontextmanager
from fastapi import FastAPI
import threading
import redis
import time
import json

r = redis.Redis(host='localhost', port=6379, decode_responses=True)

stop_threads = False

def serviceData():
    while True:
        # ดึงงานจาก queue
        data = r.rpop('data')
        if data:
            # ประมวลผลภาพ (เช่น ย่อขนาด, ใส่ลายน้ำ)
            # time.sleep(2)
            print(json.loads(data))
            r.lpush("data_resp", 200)
        global stop_threads
        if stop_threads:
            break

@asynccontextmanager
async def lifespan(app: FastAPI):
    stop_event = threading.Event()
    worker_thread = threading.Thread(target=serviceData)
    worker_thread.start()
    yield
    global stop_threads
    stop_threads = True
    stop_event.set()
    worker_thread.join(1000)

app = FastAPI(lifespan=lifespan)

@app.get("/")
async def get_root():
    return {'message':'hello server'}


@app.get("/data")
async def get_data():
    return 200
