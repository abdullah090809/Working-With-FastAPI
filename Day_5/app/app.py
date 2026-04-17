from random import randrange
import time
from typing import Optional
from fastapi import FastAPI, HTTPException, Response, status
import psycopg2
from pydantic import BaseModel, Field
from psycopg2.extras import RealDictCursor

app=FastAPI()

while(True):
    try:
        conn = psycopg2.connect(host="localhost",database="FastAPI",user="postgres",
        password="abdullah1234",cursor_factory=RealDictCursor)
        cursor=conn.cursor()
        print("Database Connected")
        break
    except Exception as error:
        print("Connection Failed")
        print(f"Error was {error}")
        time.sleep(2)


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    # rating: Optional[int] = Field(None,ge=1,le=5) Rating not in database

class PostUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    published: Optional[bool] = None
    # rating: Optional[int] = Field(None, ge=1, le=5) Rating not in database

@app.get("/posts")
def get_posts():
   cursor.execute("""SELECT * FROM posts ORDER BY id ASC""")
   posts=cursor.fetchall()
   return{
       "data": posts
   }

@app.get("/posts/{id}")
def get_post(id: int):
    cursor.execute("""SELECT * FROM posts WHERE id=%s""",(id,))
    post=cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post with {id} not Found")
    return{
        "data": post
    }

@app.post("/posts",status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    cursor.execute("""INSERT INTO posts (title,content,published) VALUES (%s,%s,%s) RETURNING *""",
    (post.title,post.content,post.published))
    new_post=cursor.fetchone()
    conn.commit()
    return{
        "data": new_post
    }

@app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute("""DELETE FROM posts WHERE id=%s RETURNING *""",(id,))
    delete_post=cursor.fetchone()
    conn.commit()
    if delete_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post with {id} does not Exit")

@app.put("/posts/{id}",status_code=status.HTTP_200_OK)
def update_post(id: int, post: Post):
    cursor.execute("""UPDATE posts SET title=%s, content=%s, published=%s WHERE id=%s RETURNING *""",
    (post.title,post.content,post.published,id))
    update_post=cursor.fetchone()
    conn.commit()
    return{
        "data": update_post
    }

@app.patch("/posts/{id}",status_code=status.HTTP_200_OK)
def update_post_patch(id: int, post: PostUpdate):
   cursor.execute("SELECT * FROM posts WHERE id=%s",(id,))
   existing_post=cursor.fetchone()
   if not existing_post:
       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post with {id} does not Exit")
   update_data=post.model_dump(exclude_unset=True)
   if not update_data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"No Field Provided")
   set_clause=", ".join([f"{key}=%s" for key in update_data.keys()])
   values=list(update_data.values())
   values.append(id)
   cursor.execute(f"""UPDATE posts SET {set_clause} WHERE id=%s RETURNING *""",
   tuple(values))
   update_post=cursor.fetchone()
   conn.commit()
   return{
       "data": update_post
   }
   

