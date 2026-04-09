from random import randrange
from typing import Optional

from fastapi import FastAPI, HTTPException, Response, status
from pydantic import BaseModel, Field

app = FastAPI()

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


def find_post(id: int):
    for p in my_post:
        if p["id"]==id:
            return p

def find_index(id: int):
    for i,p in enumerate(my_post):
        if p["id"]==id:
            return i

@app.get("/")
def home():
    return "Welcome to FastAPI Program"

@app.get("/posts")
def get_posts():
    return my_post

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    post_dict=post.dict()
    post_dict["id"]= randrange(0, 1000000)
    my_post.append(post_dict)
    return {
        "message": "Post created successfully",
        "data": post.dict()
    }

@app.get("/posts/{id}")
def get_post(id: int, response: Response):
    post=find_post(id)
    if not post:
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": f"Post with {id} not Found"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post with {id} not Found")
    return post

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id :int):
    index=find_index(id)
    if index is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with {id} not found")
    my_post.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)