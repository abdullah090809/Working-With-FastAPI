from random import randrange
from typing import Optional

from fastapi import FastAPI, HTTPException, Response, status
from pydantic import BaseModel, Field

app=FastAPI()

my_post=[
    {
        "id": 1,
        "title": "Fav Anime",
        "content": "DBS",
        "rating": 5
    },
    {
        "id": 2,
        "title": "Anime Currently Watching",
        "content": "Wind Breaker",
        "rating": 4
    }
]

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = Field(None,ge=1,le=5)

class PostUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    published: Optional[bool] = None
    rating: Optional[int] = Field(None, ge=1, le=5)

def find_post(id: int):
    for p in my_post:
        if p["id"] == id:
            return p
        
def find_index(id: int):
    for i,p in enumerate(my_post):
        if p["id"] == id:
            return i
    return None
        
@app.get("/")
def home():
    return{
        "message": "Welcome to Home Page of FASTAPI Project"
    }

@app.get("/posts")
def get_posts():
    return{
        "message": "All the Posts",
        "data": my_post
    }

@app.get("/posts/{id}")
def get_post(id: int, response: Response):
    post=find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post with {id} not Found")
    return post

@app.post("/posts",status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    post_dict=post.dict()
    post_dict["id"]=randrange(0,10000000)
    my_post.append(post_dict)
    return{
        "message": "Post Created",
        "data": post.dict()
    }

@app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    index=find_index(id)
    if index is None:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT,detail=f"Post with {id} does not Exit")
    my_post.pop(index)

@app.put("/posts/{id}",status_code=status.HTTP_200_OK)
def update_post(id: int, post: Post):
    index=find_index(id)
    if index is None:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT,detail=f"Post with {id} does not Exit")
    post_dict=post.dict()
    post_dict["id"]=id
    my_post[index]=post_dict
    return{
        "message": "Post Updated",
        "data": my_post[index]
    }

@app.patch("/posts/{id}",status_code=status.HTTP_200_OK)
def update_post_patch(id: int, post: PostUpdate):
    index=find_index(id)
    if index is None:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT,detail=f"Post with {id} does not Exit")
    update_post=post.dict(exclude_unset=True)
    my_post[index].update(update_post)
    return{
        "message": "Post Updated",
        "data": my_post[index]
    }