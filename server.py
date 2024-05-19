from contextlib import asynccontextmanager
from fastapi import FastAPI
from pydantic import BaseModel
from database.query import Query
import asyncio

import io
import base64
from PIL import Image

from model.disease_detection import AI_model
from packages.encode_decode import decode_image, encode_image

# run: uvicorn server:app --host 0.0.0.0 --port 8000 --reload

database_path = './database/data.db'
models = {}
# models['query'] = Query(database_path)

@asynccontextmanager
async def lifespan(app: FastAPI):
    models['query'] = Query(database_path)
    models['AI_model'] = AI_model(path_to_model= './model/model')

    yield

    models['query'].close()

app = FastAPI(lifespan= lifespan)

class User_Info(BaseModel):
    user_name: str
    password: str

class Image_info(BaseModel):
    image: str
    date: str
    predicted_image: str = None
    class_name: str = None
    class_prob: float  = None

class Analyze(BaseModel):
    user_info: User_Info
    image_info : Image_info

@app.post("/check-login")
async def check_login(item: User_Info):
    # print(dict(item))
    response = await models['query'].user_login(item)
    # print(response)
    return response

@app.post("/create-new-user")
async def create_new_user(item: User_Info):
    # print(dict(item))
    response = await models['query'].add_user(item)
    # print(response)
    return response

@app.post("/get-history")
async def get_history(item: User_Info):
    response = await models['query'].get_history(item)
    return response

@app.post("/analyze")
async def analyze(item: Analyze):
    image = decode_image(item.image_info.image)
    result = await models['AI_model'].predict(image)
    # print(result['class_name'])
    item.image_info.class_name = result['class_name']
    item.image_info.class_prob = result['class_prob']
    item.image_info.predicted_image = encode_image(result['predicted_image'])

    response = await models['query'].add_pic_and_get_solution(item)
    # print(response['solution'])
    return response