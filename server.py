from contextlib import asynccontextmanager
from fastapi import FastAPI
from pydantic import BaseModel
from database.query import Query

# run: uvicorn server:app --host 0.0.0.0 --port 8000 --reload

database_path = './database/data.db'
models = {}

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load the ML model
    print('starting..................')
    # query = Query(database_path)
    models['query'] = Query(database_path)
    yield
    # Clean up the ML models and release the resources
    print('shuting down..................')

app = FastAPI(lifespan= lifespan)
request = {
    'user_info': {
        'info': {
            'user_name' : 'admin',
            'password' : b'admin'
        }
    },
    'image' : 'ma hinh anh',
    'date' : 'DD-MM-YYYY'
}

class User_Info(BaseModel):
    user_name: str
    password: str

class Request_API(BaseModel):
    user_info: dict[str, User_Info]
    image: str
    date: str

@app.post("/check-login")
async def check_login(item: User_Info):
    print(dict(item))
    response = await models['query'].user_login(item)
    print(response)
    return response

@app.post("/create-new-user")
async def create_new_user(item: User_Info):
    print(dict(item))
    response = await models['query'].add_user(item)
    print(response)
    return response




# @app.on_event("shutdown")
# async def shutdown_event():
#     print("Server is shutting down...")

# @app.post("/analyze")
# async def check_login(item: User_Info):
#     print(dict(item))
#     response = query.user_login(item, database_path)
#     return response