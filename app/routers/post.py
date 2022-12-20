from .. import models, schemas, oauth2
from typing import List, Optional
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..database import get_db
from sqlalchemy import func


# The purpose of adding prefix and passing /posts is to avoid duplication of work.
# For example if we have large number of apis and everyapi starts with /posts and if we need to replace posts with some other prefix it would be difficult to change that in all the routes. To avoid this we use prefix.
# We know fast api provides auto documentation. In our current project we have separate routes for userSignUp and posts. We will not use the tags in swagger we get all the routes jumbled. To separate the routes we can use tags
router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)

# @router.get("/",response_model=List[schemas.Post])
@router.get("/",response_model=List[schemas.PostOut])
async def my_post(db:Session = Depends(get_db),user_id:int=Depends(oauth2.get_current_user),limit:int=10,skip:int=0,search:Optional[str]=""):
    posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    # We used postgres joins in the below line
    results = db.query(models.Post,func.count(models.Vote.post_id).label("votes")).join(models.Vote,models.Vote.post_id==models.Post.id,isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    return results

@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.Post)
# def create_posts(payload:dict=Body(...)):
async def create_posts(post:schemas.PostCreate, db:Session = Depends(get_db),user_id:int = Depends(oauth2.get_current_user)):
    # It would be difficult to pass the body individually same as below line if we have many columns
    # new_post =  models.Post(title=post.title,content = post.content, published = post.published)
    
    # Inorder to do it in the dynamic way we need to user .dict() and pass the dict after upacking it using **
    new_post = models.Post(owner_id=user_id.id,**post.dict())
    # Adding the post to the DB
    db.add(new_post)
    # commit the post to DB
    db.commit()
    # After commit the changes to fetch the created post use the below line
    db.refresh(new_post)
    return new_post


# HTTPException is used to handle errors and status codes
@router.get("/{id}",response_model=schemas.PostOut)
def get_post(id:int,db:Session=Depends(get_db)):
    # post = db.query(models.Post).filter(models.Post.id == id).first()
    post = db.query(models.Post,func.count(models.Vote.post_id).label("votes")).join(models.Vote,models.Vote.post_id==models.Post.id,isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post with id: {id} not found")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"Message":f"post with id: {id} was not found"}
    return post


@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int,db:Session=Depends(get_db),user_id:int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id==id) 
    post = post_query.first()   
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post with id: {id} doesnot exists")
    if post.owner_id != user_id.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not authorized to perform requested action.")
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
    

@router.put("/{id}",response_model=schemas.Post)
def update_posts(id:int,updated_post:schemas.PostCreate,db:Session=Depends(get_db),user_id:int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post with id: {id} doesnot exists")
    if post.owner_id != user_id.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not authorized to perform requested action.")
    post_query.update(updated_post.dict(),synchronize_session=False)
    db.commit()
    return post_query.first()