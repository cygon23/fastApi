from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from  fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from dotenv import load_dotenv
import os


app = FastAPI()

class Post(BaseModel):
    title:str
    content:str
    published:bool = True
    rating: Optional[int] = None

    load_dotenv()


# Get variables
host = os.getenv("DB_HOST")
database = os.getenv("DB_NAME")
user = os.getenv("DB_USER")
password = os.getenv("DB_PASS")


while True:
##connect to the db
   try:
       conn = psycopg2.connect(
    host=host,
    database=database,
    user=user,
    password=password,
    cursor_factory=RealDictCursor
)
       cursor = conn.cursor()
       print("Database connection was succefully")
       break
   except Exception as error:
       print("connecting to databse failed")
       print("Error", error)
       time.sleep(2)


my_posts = [{
    "title":"title of the post","content": "content of post 1", "id":1},
     {"title":"title of the post","content": "content of post 2", "id":2}
     ]
def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p

def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i
        

@app.get("/")
async def root():
    return{"message": "hellow world as usuall"} 

@app.get("/posts")
def get_posts():
    cursor.execute(""" SELECT * FROM posts """)
    posts =cursor.fetchall()
    return {"data": my_posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post:Post):
    post_dict = post.dict()
    post_dict['id'] = randrange(0, 100000)
    my_posts.append(post_dict)
    return {"data": post_dict}

@app.get("/posts/{id}")
def get_post(id: int):
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")
    return {"post_details": post}
    

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    index = find_index_post(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")
    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    index = find_index_post(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")
    post_dict = post.dict()
    post_dict['id'] = id
    my_posts[index] = post_dict
    return {'data': post_dict}