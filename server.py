from contextlib import asynccontextmanager
from fastapi import FastAPI
from pydantic import BaseModel
from database.query import Query
import asyncio

import io
import base64
from PIL import Image

from model.disease_detection import AI_model
from model.disease_detection import Cnn_model
from packages.encode_decode import decode_image, encode_image

# run: uvicorn server:app --host 0.0.0.0 --port 8000 --reload

database_path = './database/data.db'
models = {}
# database = Query(database_path)

disease_detector = None
database = None
leaf_or_not_detector = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global disease_detector
    global database
    global leaf_or_not_detector
    
    database = Query(database_path)
    disease_detector = AI_model(path_to_model= './model/models/tomato_disease')
    leaf_or_not_detector = Cnn_model(path_to_model='./model/models/leaf_or_not')
    yield

    database.close()

app = FastAPI(lifespan= lifespan)

class User_Info(BaseModel):
    user_name: str
    password: str

class Image_info(BaseModel):
    image: str
    date: str
    predicted_image: str = None
    class_name: str = None
    score: float  = None
    threshold: float  = None
    garden_num: int  = None
    line_num: int  = None
    

class Analyze(BaseModel):
    user_info: User_Info
    image_info : Image_info

class Change_password(BaseModel):
    user_info: User_Info
    new_password: str = None

class Get_statistics(BaseModel):
    user_info: User_Info
    date: str
    gardenNum: int
    lineNum: int

class Add_new_user(BaseModel):
    user_info: User_Info
    new_user_info: User_Info

class Garden_info(BaseModel):
    plant_name : str
    garden_name : str
    num_of_line : int

class Add_garden(BaseModel):
    user_info: User_Info
    garden_info: Garden_info

class Get_gardens_info(BaseModel):
    user_info: User_Info

class Get_employee_info(BaseModel):
    user_info: User_Info   

@app.post("/check_login")
async def check_login(item: User_Info):
    # print(dict(item))
    response = await database.user_login(item)
    # print(response)
    return response

@app.post("/create_new_user")
async def create_new_user(item: Add_new_user):
    # print(dict(item))
    response = await database.add_user(item.user_info, item.new_user_info)
    # print(response)
    return response

@app.post("/get_history")
async def get_history(item: User_Info):
    response = await database.get_history(item)
    return response

@app.post("/analyze")
async def analyze(item: Analyze):
    image = decode_image(item.image_info.image)

    leaf_result = await leaf_or_not_detector.predict(img=image)

    if leaf_result['predicted_class'] != 'leaf':
    # if leaf_result['predicted_class'] != 'leaf' and disease_result['score'] < disease_result['threshold']:
        item.image_info.class_name = None
        item.image_info.score = None
        item.image_info.threshold = None
        item.image_info.predicted_image = None
        response = item
    else:
        disease_result = await disease_detector.predict(img=image)
        
        item.image_info.class_name = disease_result['class_name']
        item.image_info.score = disease_result['score']
        item.image_info.threshold = disease_result['threshold']
        item.image_info.predicted_image = encode_image(disease_result['predicted_image'])


        response = await database.add_pic_and_get_solution(item= item, is_save=True)
    return response

@app.post("/change_password")
async def change_password(item: Change_password):
    response = await database.change_password(item)
    return response

@app.post("/get_statistics")
async def get_statistics(item: Get_statistics):
    response = await database.get_statistic(item)
    return response

@app.post("/get_all_solutions")
async def get_all_solutions():
    response = await database.get_solution()
    return response

@app.post("/add_garden")
async def add_garden(item: Add_garden):
    response = await database.add_garden(item)
    return response

@app.post("/get_gardens_info")
async def get_gardens_info(item: Get_gardens_info):
    response = await database.get_garden_info(item)
    return response

@app.post("/get_employee_info")
async def get_employee_info(item: Get_employee_info):
    response = await database.get_garden_info(item)
    return response