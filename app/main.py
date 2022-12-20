from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
# Pydantic is used for defining schema
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time

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
    cursor.execute("""SELECT * FROM "apiData" """)
    posts = cursor.fetchall()
    print(posts,"posts")
    return {"data":posts}

@app.post("/posts",status_code=status.HTTP_201_CREATED)
# def create_posts(payload:dict=Body(...)):
async def create_posts(post:Post):
    # We should never pass directly data in the below format, because user may enter "INSERT INTO ***" which causes SQL injection attack
    # cursor.execute(f"INSERT INTO apiData (title,content,published) VALUES ({post.title},{post.content},{post.published})")
    cursor.execute("""INSERT INTO "apiData" (title, content, published) VALUES (%s, %s, %s) RETURNING * """,(post.title,post.content,post.published))
    new_post = cursor.fetchone()
    # Below line is used to commit the changes to DB
    conn.commit()
    return {"data":new_post}


# Defining the order of routes is important, fo example we have a route "posts/{id}" and another route "post/latest" when ever we make a request for "posts/latest" it will be routed to "posts/{id}". So, ordering is important.
@app.get("/posts/latest")
def get_latest_post():
    cursor.execute("""SELECT * FROM "apiData" """)
    latestPost = cursor.fetchone()
    return {"data":latestPost}

# HTTPException is used to hnadle errors and status codes

@app.get("/posts/{id}")
def get_post(id:str):
    cursor.execute("""SELECT * from "apiData" WHERE id = %s """,(str(id),))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post with id: {id} not found")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"Message":f"post with id: {id} was not found"}
    return {"data":post}


@app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:str):
    cursor.execute("""DELETE FROM "apiData" WHERE id = %s RETURNING * """,(str(id),))
    deleted_post = cursor.fetchone()
    conn.commit()
    if not delete_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post with id: {id} doesnot exists")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
    

@app.put("/posts/{id}")
def update_posts(id:int,post:Post):
    cursor.execute("""UPDATE "apiData" SET title = %s, content = %s, published = %s WHERE id = %s RETURNING * """,(post.title,post.content,post.published,str(id)))
    updatedPost = cursor.fetchone()
    conn.commit()
    
    if not updatedPost:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post with id: {id} doesnot exists")
    
    
    return {"data":updatedPost}