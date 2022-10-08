from statistics import mode
from .. import schemas, utils, models
from fastapi import FastAPI, Response , status, HTTPException, Depends, APIRouter
from ..database import get_db
from sqlalchemy.orm import Session
from typing import List

router = APIRouter(
    prefix="/users",
    tags = ['Users']
    )

@router.post("/" , status_code=status.HTTP_201_CREATED , response_model= schemas.UserOut)
def createUser(user: schemas.UserCreate , db: Session = Depends(get_db)):
    
    try:
        hashed_password = utils.hash(user.password)
        user.password = hashed_password
        new_user = models.User(**user.dict())
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return  new_user
    except:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"User account with email {user.email} already exits")

@router.get("/")
def getUsers(db: Session = Depends(get_db)):

    users_query = db.query(models.User)
    users = users_query.all()

    return users

@router.get("/{id}" , response_model=schemas.UserOut)
def getUser(id:int, db: Session = Depends(get_db)):

    users_query = db.query(models.User).filter(models.User.id == id)
    user = users_query.first()

    if user==None:

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"no user with id {id}")

    return user