from .. import models , schemas, utils , oauth2
from fastapi import FastAPI, Response , status, HTTPException, Depends, APIRouter
from ..database import get_db
from sqlalchemy.orm import Session
from typing import List, Optional
from sqlalchemy import func

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
    )


@router.get("/" , response_model= List[schemas.Postwithvotes])
def get_post(db: Session = Depends(get_db), limit: int = 10, skip: int = 0 ,
search: Optional[str] = ''):
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()
    # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    posts = db.query(models.Post , func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id==models.Post.id , isouter = True).group_by(models.Post.id).filter(
            models.Post.title.contains(search)).limit(limit).offset(skip).all()
    
    return posts

@router.post("/", status_code=status.HTTP_201_CREATED, response_model= schemas.Post)
def make_post(new_post: schemas.PostCreate, db: Session = Depends(get_db) , current_user: int = Depends(
    oauth2.get_current_user)):
    
    # cursor.execute("""INSERT INTO posts (title, content, published) 
    # VALUES (%s, %s, %s) RETURNING *""", (new_post.title, new_post.content, new_post.published))
    # conn.commit()
    # new = cursor.fetchone()
    # print(current_user.email)
    new = models.Post(user_id=current_user.id, **new_post.dict() )
    db.add(new)
    db.commit()
    db.refresh(new)
    return  new


@router.get("/latest" , response_model= schemas.Postwithvotes)
def get_latest_post(db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts ORDER BY id DESC""")
    # last_post = cursor.fetchone()
    # post_query = db.query(models.Post).order_by(models.Post.id.desc())

    post_query = db.query(models.Post , func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id==models.Post.id , isouter = True).group_by(
            models.Post.id).order_by(models.Post.id.desc())
    last_post = post_query.first()
    return last_post


@router.get("/{id}" , response_model= schemas.Postwithvotes)
def get_one_post(id: int , response: Response , db: Session = Depends(get_db)):
    
    # cursor.execute("""SELECT * from posts WHERE id = %s""", (str(id)))
    # post = cursor.fetchone()
    # post = db.query(models.Post).filter(models.Post.id == id).first()

    post = db.query(models.Post , func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id==models.Post.id , isouter = True).group_by(
            models.Post.id).filter(models.Post.id == id).first()
    # print(post)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="LOL" )
        # response.status_code = status.HTTP_404_NOT_FOUND

    return post


@router.delete("/{id}" , status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int ,db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""",(str(id)) )
    # ind = cursor.fetchone()
    # conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id)
    
    post = post_query.first()

    if post ==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"no post with id {id}")

    if post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=
        "Not authorised to perform the requested task")
    
    post_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}" , response_model= schemas.Post,)
def update_post(id: int , post: schemas.PostCreate , db: Session = Depends(get_db), 
    current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""UPDATE posts SET title = %s , content = %s, published = %s WHERE id = %s 
    #                 RETURNING *""", (post.title, post.content, post.published, str(id)))
    # chosen_post = cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post_current = post_query.first()

    if post_current==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"no post with id {id}")

    
    if post_current.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorised to perform the requested task")
    
    
    post_query.update(post.dict() , synchronize_session=False)
    db.commit()
    return post_query.first()