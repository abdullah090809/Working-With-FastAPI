from fastapi import APIRouter, HTTPException, Depends, status, Response
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.posts import Post
from app.models.users import User
from app.oauth2 import Get_Current_User
from app.schemas.post import PostCreate, PostUpdate, PostResponse

router = APIRouter(prefix="/posts", tags=["Posts"])

@router.get("/", response_model=list[PostResponse])
def get_posts(db: Session = Depends(get_db), current_user: User= Depends(Get_Current_User)):
    return db.query(Post).all()

@router.post("/", response_model=PostResponse)
def create_post(post: PostCreate, db: Session = Depends(get_db), current_user: User= Depends(Get_Current_User)):
    new_post = Post(owner_id=current_user.id,**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.get("/{id}", response_model=PostResponse)
def get_post(id: int, db: Session = Depends(get_db),current_user: User= Depends(Get_Current_User)):
    post = db.query(Post).filter(Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} does not exist")
    return post

@router.delete("/{id}")
def delete_post(id: int, db: Session = Depends(get_db), current_user: User = Depends(Get_Current_User)):
    post_query = db.query(Post).filter(Post.id == id)
    post = post_query.first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} does not exist")
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not Authorized to Perform this Action")
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}", response_model=PostResponse)
def update_post(id: int, updated_post: PostCreate, db: Session = Depends(get_db), current_user: User = Depends(Get_Current_User)):
    post_query = db.query(Post).filter(Post.id == id)
    post = post_query.first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} does not exist")
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not Authorized to Perform this Action")
    post_query.update(updated_post.model_dump(), synchronize_session=False)
    db.commit()
    return post_query.first()

@router.patch("/{id}", response_model=PostResponse)
def update_post_patch(id: int, updated_post: PostUpdate, db: Session = Depends(get_db), current_user: User = Depends(Get_Current_User)):
    post_query = db.query(Post).filter(Post.id == id)
    post = post_query.first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} does not exist")
    if post.owner_id != current_user.id:  # ← use post, not post_query
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not Authorized to Perform this Action")
    post_query.update(updated_post.model_dump(exclude_unset=True), synchronize_session=False)
    db.commit()
    return post_query.first()