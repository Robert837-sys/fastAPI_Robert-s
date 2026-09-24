from fastapi import FastAPI,Response,HTTPException,status,Depends
from fastapi.params import Body
from pydantic import BaseModel 
from typing import Optional,List
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from . import models,schemas
from .database import engine,get_db

models.Base.metadata.create_all(bind=engine)

app=FastAPI()


 
    
while True:     
    try:
        conn=psycopg2.connect(host='localhost',database='fastAPI',user='postgres',password='Agie@2015',cursor_factory=RealDictCursor)
        cursor=conn.cursor()
        print("Database connection was successfull!")
        break
    except Exception as error:
        print("Connection to database failed")
        print("Error: ",error)
        time.sleep(2)
    
# my_posts=[{"title":"title of post 1","content":"content of post 1","id":1},{"title":"favorite foods","content":"I like pizza","id":2}]

@app.get("/")
def root():
    return {"message":"welcome to my api!!!!"}
# def read_root():
#     return {"Hello": "World"}



    

# @app.get("/posts")
# def get_posts():
#     return {"data":my_posts}


# @app.post("/cposts")
# def create_posts(post: Post):
#     post_dict=post.model_dump()
#     # print(new_post.published )
#     # print(new_post.model_dump() )
#     # return {"data":"new post"}
#     post_dict['id']=randrange(0,1000000)
#     my_posts.append(post_dict.model_dump())
#     return {"data":post_dict}



# title str, content str

# Revision, delete after practice

@app.post("/createposts",status_code=status.HTTP_201_CREATED)
def create_posts(post:schemas.Post):
    post_dict=post.model_dump()
    post_dict['id']=randrange(0,1000000)
    my_posts.append(post_dict)
    return {"data":post_dict}

# hit post request again

# after all that hit send again







# CRUD Applications

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

@app.get("/posts12")
def get_posts(db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM post """)
    # posts=cursor.fetchall()
    posts=db.query(models.Post).all()
    return posts


@app.post("/posts1",status_code=status.HTTP_201_CREATED,response_model=schemas.Post)
def create_posts(post:schemas.PostCreate,db: Session = Depends(get_db)):
    # """
    # cursor.execute(""" INSERT INTO posts (title,content,published) VALUES (%s,%s,%s) RETURNING * """,(post.title,post.content,post.published))
    # new_post=cursor.fetchone()
    # post_dict=post.model_dump()
    # post_dict['id']=randrange(0,1000000)
    # my_posts.append(post_dict)
    # conn.commit()
    # """
    # print(**post.model_dump())
    new_post=models.Post(**post.model_dump())
    # new_post=models.Post(title=post.title,content=post.content,published=post.published)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@app.get("/posts99/{id}",response_model=schemas.Post)
def get_post(id: int,db:Session=Depends(get_db)):
    # 
    # """cursor.execute("""SELECT * FROM posts WHERE id=%s""",(str(id)))
    # test_post=cursor.fetchone()
    # print(test_post)
    # print(type(id))
    # post=find_post(id)
    # """
    # 
    
    post=db.query(models.Post).filter(models.Post.id==id).first()
    
    if not post:
        # response.status_code=status.HTTP_404_NOT_FOUND
        # return {"message":f"post with id: {id} wasn't found"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id {id} was not found")
    
    return post

@app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int,db:Session=Depends(get_db)):
    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING * """,(str(id)))
    # deleted_post=cursor.fetchone()
    # # index=find_index_post(id)
    # conn.commit()
    
    post_query=db.query(models.Post).filter(models.Post.id==id)
    post=post_query.first()
    
    
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post with id {id} doesn't exist.")
    
    # my_posts.pop(index)
    # return {'message':'post was successfully deleted'}
    post_query.delete(synchronize_session=False)
    db.commit()
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}",response_model=schemas.Post)
def update_post(id: int,updated_post: schemas.PostCreate,db:Session=Depends(get_db)):
    
    # cursor.execute("""UPDATE posts SET title=%s,content=%s,published=%s WHERE id = %s RETURNING *""",(post.title,post.content,post.published,str(id)))
    # update_post=cursor.fetchone()
    # index=find_index_post(id)
    # conn.commit()
    post_query= db.query(models.Post).filter(models.Post.id==id)
    post=post_query.first()
    
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post with id {id} doesn't exist.")
    # print(post)
    # post_dict=post.model_dump()
    # post_dict['id']=id
    # my_posts[index]=post_dict
    post_query.update(updated_post.model_dump(),synchronize_session=False)
    
    db.commit()
    
    return post_query.first()


# 