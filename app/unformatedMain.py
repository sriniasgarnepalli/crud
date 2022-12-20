from typing import Optional, List
from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
# Pydantic is used for defining schema
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . import models, schemas, utils
from .database import engine, get_db
from sqlalchemy.orm import Session


models.Base.metadata.create_all(bind=engine)
app = FastAPI()


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
    


@app.get("/myposts",response_model=List[schemas.Post])
async def my_post(db:Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts

@app.post("/posts",status_code=status.HTTP_201_CREATED,response_model=schemas.Post)
# def create_posts(payload:dict=Body(...)):
async def create_posts(post:schemas.PostCreate, db:Session = Depends(get_db)):
    # It would be difficult to pass the body individually same as below line if we have many columns
    # new_post =  models.Post(title=post.title,content = post.content, published = post.published)
    
    # Inorder to do it in the dynamic way we need to user .dict() and pass the dict after upacking it using **
    new_post = models.Post(**post.dict())
    # Adding the post to the DB
    db.add(new_post)
    # commit the post to DB
    db.commit()
    # After commit the changes to fetch the created post use the below line
    db.refresh(new_post)
    return new_post


# HTTPException is used to handle errors and status codes
@app.get("/posts/{id}",response_model=schemas.Post)
def get_post(id:int,db:Session=Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post with id: {id} not found")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"Message":f"post with id: {id} was not found"}
    return post


@app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int,db:Session=Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id==id)    
    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post with id: {id} doesnot exists")
    
    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
    

@app.put("/posts/{id}",response_model=schemas.Post)
def update_posts(id:int,updated_post:schemas.PostCreate,db:Session=Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post with id: {id} doesnot exists")
    
    post_query.update(updated_post.dict(),synchronize_session=False)
    db.commit()
    return post_query.first()


@app.post("/signup",status_code=status.HTTP_201_CREATED,response_model=schemas.UserOut)
def create_user(user:schemas.CreateUser,db:Session=Depends(get_db)):
    # Creating hash of the password
    hashed_password = utils.hash(user.password)
    # In the below line we are setting the password with hashed value
    user.password = hashed_password
    
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.get("/users/{id}",response_model=schemas.UserOut)
def get_user_details(id:int,db:Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id==id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"User with {id} doesnot exist")
    return user