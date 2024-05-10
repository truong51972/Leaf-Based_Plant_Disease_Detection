from fastapi import FastAPI
from pydantic import BaseModel


# run: uvicorn api_server/main:app --host 0.0.0.0 --port 8000
request= {
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
    password: bytes

class Request_API(BaseModel):
    user_info: dict['info', User_Info]
    image: str
    date: str


app = FastAPI()


@app.post("/api")
async def create_item(item: Request_API):
    return {'Chao': 'em'}