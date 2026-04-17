from fastapi import FastAPI, HTTPException, Depends, status, Response
from sentry_sdk import HttpTransport
from sqlalchemy.orm import Session
from app.database import Base, get_db, engine
from app.models.posts import Post
from app.schemas.post import PostCreate, PostUpdate

Base.metadata.create_all(bind=engine)


app=FastAPI()

@app.get("/")
def home():
    return{
        "message": "Welcome to FastAPI Project"
    }

@app.get("/posts")
def get_post(db: Session = Depends(get_db)):
    post=db.query(Post).all()
    return{
        "data": post
    }

@app.post("/posts")
def create_post(post: PostCreate, db: Session = Depends(get_db)):
    new_post=Post(**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return{
        "data": new_post
    }

@app.get("/posts/{id}")
def get_post(id : int, db: Session = Depends(get_db)):
    post=db.query(Post).filter(Post.id==id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post with id {id} does not Exit")
    return{
        "data": post
    }

@app.delete("/posts/{id}")
def delete_post(id: int, db: Session = Depends(get_db)):
    post=db.query(Post).filter(Post.id==id)
    if not post.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post with id {id} does not Exit")
    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id:int, updated_post: PostCreate, db: Session = Depends(get_db)):
    post_query=db.query(Post).filter(Post.id==id)
    post=post_query.first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post with id {id} does not Exit")
    post_query.update(updated_post.model_dump(),synchronize_session=False)
    db.commit()
    return{
        "data": post_query.first()
    }

@app.patch("/posts/{id}")
def update_post_using_patch(id: int , updated_post: PostUpdate, db: Session = Depends(get_db)):
    post_query=db.query(Post).filter(Post.id==id)
    post=post_query.first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post with id {id} does not Exit")
    post_query.update(updated_post.model_dump(exclude_unset=True),synchronize_session=False)
    db.commit()
    return{
        "data": post_query.first()
    }
