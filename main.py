from fastapi import FastAPI,UploadFile,Form,Response
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
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
                place:Annotated[str,Form()],
                insertAt:Annotated[int,Form()]
                ):
    image_bytes = await image.read() #image는 큰 데이터로 오기때문에 읽는과정에서 await이 필요
    # SQL문법▼items테이블중(title,image,price,description,place)에 VALUES ('{title}','{image_bytes.hex()}','{price}','{description}','{place}')값을 넣겠다#
    cur.execute(f"""
                INSERT INTO 
                items(title,image,price,description,place,insertAt) 
                VALUES ('{title}','{image_bytes.hex()}',{price},'{description}','{place}',{insertAt}) 
                """) #SQL
    con.commit() #데이터들어가짐
    return '200'

@app.get('/items')
async def get_items():  #컬럼명도 같이가져옴
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    rows = cur.execute(f"""
                       SELECT * from items;
                       """).fetchall()
    return JSONResponse(jsonable_encoder(dict(row)for row in rows)) #dict_객체형태로바꿔줌


@app.get('/images/{item_id}')
async def get_image(item_id):
    cur = con.cursor()
    image_bytes = cur.execute(f"""
                              SELECT image from items WHERE id={item_id}
                              """).fetchone()[0]  #.fetchone()[0] 한개만 불러오는
    return Response(content=bytes.fromhex(image_bytes))  #img를가져와서 컨텐츠로변환해주는



app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")