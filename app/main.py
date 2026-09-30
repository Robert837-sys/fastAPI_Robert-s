from fastapi import FastAPI,Response,HTTPException,status,Depends
from fastapi.params import Body
from pydantic import BaseModel 
from typing import Optional,List
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from . import models,schemas,utils
from .database import engine,get_db
from .routers import post,user,auth



models.Base.metadata.create_all(bind=engine)

app=FastAPI()

app.include_router(post.router)   
app.include_router(user.router)
app.include_router(auth.router)

@app.get("/")
def root():
    return {"message":"welcome to my api!!!!"}

# """
# @app.post("/createposts",status_code=status.HTTP_201_CREATED)
# def create_posts(post:schemas.Post):
#     post_dict=post.model_dump()
#     post_dict['id']=randrange(0,1000000)
#     my_posts.append(post_dict)
#     return {"data":post_dict}
# """


my_posts=[{"title":"title of post 1","content":"content of post 1","id":1},{"title":"favorite foods","content":"I like pizza","id":2}]

def find_post(id):
    for p in my_posts:
        if p["id"]==id:
            return p
        
def find_index_post(id):
    for i,p in enumerate(my_posts):
        if p['id']==id:
            return i

@app.get("/")
def root():
    return {"message":"welcome to my api!!!!"}



@app.post("/login")
def login(credentials: schemas.UserLogin,db:Session=Depends(get_db)):
    user=db.query(models.User).filter(models.User.email==credentials.email).first()
    
    if not user or not utils.verify_password(credentials.password,user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid credentials")
    return {"message":"Login successful"}
  
