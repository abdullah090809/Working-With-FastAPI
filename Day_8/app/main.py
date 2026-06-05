from fastapi import FastAPI
from app.database import Base, engine
from app.routers import post, user, auth, vote

app = FastAPI()

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get("/")
def home():
    return "FastAPI Project"