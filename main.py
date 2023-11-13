from fastapi import FastAPI,UploadFile,Form
from fastapi.staticfiles import StaticFiles
from typing import Annotated
import sqlite3

con = sqlite3.connect('db.db',check_same_thread=False)
cur = con.cursor()


app = FastAPI()

@app.post('/items')
async def create_item(image:UploadFile,
                title:Annotated[str,Form()],
                price:Annotated[int,Form()],
                description:Annotated[str,Form()],
                place:Annotated[str,Form()]):
    image_bytes = await image.read() #image는 큰 데이터로 오기때문에 읽는과정에서 await이 필요
    # SQL문법▼items테이블중(title,image,price,description,place)에 VALUES ('{title}','{image_bytes.hex()}','{price}','{description}','{place}')값을 넣겠다#
    cur.execute(f"""
                INSERT INTO items(title,image,price,description,place) 
                VALUES ('{title}','{image_bytes.hex()}',{price},'{description}','{place}')
                """)
    con.commit() #데이터들어가짐
    return '200'

app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")