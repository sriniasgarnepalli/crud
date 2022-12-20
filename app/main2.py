from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
# Pydantic is used for defining schema
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from .config import settings

app = FastAPI()

# Schema
class Post(BaseModel):
    title: str
    content:str
    published:bool = True
    
    
# In postgres while making a connection we need to pass cursor_factory=RealDictCursor without which we cannot get column name and value
while True:
    try:
        conn = psycopg2.connect(host="",database="",user="",password="",cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Connection Successful")
        break
    except Exception as error:
        print("Connecting to database failed")
        print("error",error)
        time.sleep(2)
    
my_posts = [{"title":"title of post1","content":"Content of post1","id":1},{"title":"Fav Actor","content":"Ramcharan","id":2}]

def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p
        
        
def find_post_to_delete(id):
    for i, p in enumerate(my_posts):
        if p["id"] == id:
            return i



@app.get("/myposts")
async def my_post():
    return {"data":my_posts}

@app.post("/posts",status_code=status.HTTP_201_CREATED)
# def create_posts(payload:dict=Body(...)):
def create_posts(post:Post):
    post_dict = post.dict()
    post_dict["id"] = randrange(0,99999)
    my_posts.append(post_dict)
    # print(new_post.dict())
    # return {"new_post":f"{payload['title']} {payload['content']}"}
    return {"data":post_dict}


# Defining the order of routes is important, fo example we have a route "posts/{id}" and another route "post/latest" when ever we make a request for "posts/latest" it will be routed to "posts/{id}". So, ordering is important.
@app.get("/posts/latest")
def get_latest_post():
    post = my_posts[len(my_posts)-1]
    return {"data":post}

# HTTPException is used to hnadle errors and status codes

@app.get("/posts/{id}")
def get_post(id:int,response:Response):
    print("inside get")
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post with id: {id} not found")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"Message":f"post with id: {id} was not found"}
    return {"data":post}


@app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int):
    index = find_post_to_delete(id)
    if not index:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post with id: {id} doesnot exists")
    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
    

@app.put("/posts/{id}")
def update_posts(id:int,post:Post):
    index = find_post_to_delete(id)
    if not index:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post with id: {id} doesnot exists")
    
    post_dict = post.dict()
    post_dict["id"] = id
    my_posts[index] = post_dict
    return {"data":post_dict}