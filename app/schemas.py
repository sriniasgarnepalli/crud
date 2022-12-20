from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional    
from pydantic.types import conint
    
class PostBase(BaseModel):
    title:str
    content:str
    published:bool = True
    
class PostCreate(PostBase):
    pass

# In order to avoid duplication of fields in the Post class we can use the existing fields from PostBase class and fields which are not availble in PostBase class
# class Post(BaseModel):
#     id:int
#     title:str
#     content:str
#     published:bool
#     created_at: datetime

class UserOut(BaseModel):
    id:int
    email:EmailStr
    created_at: datetime
    
    class Config:
        orm_mode = True
    
class Post(PostBase):
    id:int
    created_at: datetime
    owner_id : int
    owner:UserOut
    
    class Config:
        orm_mode = True
        

class PostOut(BaseModel):
    Post: Post
    votes: int
    
    class Config:
        orm_mode = True
        
        
class CreateUser(BaseModel):
    email:EmailStr
    password:str
            

class UserLogin(BaseModel):
    email:EmailStr
    password:str
    
class Token(BaseModel):
    access_token:str
    token_type:str
    
class TokenData(BaseModel):
    id: Optional[str] = None
    
    
# conint is used to handle vote value le=1 will allow anything lessthan 1, try to handle the below schema to handle only 0 or 1 as input
class Vote(BaseModel):
    post_id:int
    dir:conint(le=1)