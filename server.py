from fastapi import FastAPI
from pydantic import BaseModel

# run: uvicorn main:app --host 0.0.0.0 --port 8000
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
    response = {
        'status': 'oki',
    }
    return response
