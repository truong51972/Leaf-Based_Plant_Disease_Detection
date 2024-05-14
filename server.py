from contextlib import asynccontextmanager
from fastapi import FastAPI
from pydantic import BaseModel
from database.query import Query
import asyncio


# run: uvicorn server:app --host 0.0.0.0 --port 8000 --reload

database_path = './database/data.db'
models = {}
# models['query'] = Query(database_path)

@asynccontextmanager
async def lifespan(app: FastAPI):
    models['query'] = Query(database_path)
    # Load the ML model
    print('Setup Successfully!')
    # query = Query(database_path)
    yield
    # Clean up the ML models and release the resources
    Query.close()
    print('Shut Down!')

app = FastAPI(lifespan= lifespan)

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