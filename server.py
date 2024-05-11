from fastapi import FastAPI
from pydantic import BaseModel
from database import query

# run: uvicorn server:app --host 0.0.0.0 --port 8000 --reload
app = FastAPI()

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
    # response = {
    #     'status': 'oki',
    # }
    print(item.user_name)
    print(item.password)
    response = query.check_password(item.user_name, item.password)
    return response
