from fastapi import FastAPI
from pydantic import BaseModel
import  redis
import time
import json

r = redis.Redis(host='localhost', port=6379, decode_responses=True)


app = FastAPI()


class Data(BaseModel):
    username: str
    age: int


@app.get("/")
async def get_root():
    return {'message': "Hello client"}



@app.post("/data")
async def get_data(data: Data):
    resp = handlerData(data)
    return resp

    
def handlerData(data: Data):
    #producer
    r.lpush("data", data.model_dump_json())

    resp = r.rpop("data_resp")
    return resp

# def serviceData():
#     while True:
#         # ดึงงานจาก queue
#         data = r.rpop('data')

#         if data:
#             # ประมวลผลภาพ (เช่น ย่อขนาด, ใส่ลายน้ำ)
#             time.sleep(2)
#             print(json.loads(data))
#             return json.loads(data)
#         else:
#             # ถ้าไม่มีงานใน queue ให้รอเวลาสักครู่
#             time.sleep(1)

