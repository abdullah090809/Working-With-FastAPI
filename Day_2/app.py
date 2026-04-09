from typing import Optional

from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel, Field


app=FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = Field(None, ge=1, le=5)


@app.get("/")
def home():
    return "Hello World"

@app.post("/post")
def createpost(post: Post):
    post=post.dict()
    return post