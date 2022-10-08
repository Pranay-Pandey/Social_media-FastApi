from os import access
from statistics import mode
from fastapi import APIRouter, Response, HTTPException, Depends, status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ..database import get_db
from .. import schemas, models, utils, oauth2

router = APIRouter(tags=['Authentication'])

@router.post('/login' , response_model=schemas.Token)
def login(user: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):


    requestd_user = db.query(models.User).filter(models.User.email==user.username).first()

    if not requestd_user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"no user with email {user.username}")

    if not utils.verify(user.password, requestd_user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"incorrect password for email {user.username}")

    #MAKE TOKEN

    #return token

    access_token = oauth2.create_access_token(data = {"user_id": requestd_user.id})
    return {"access_token": access_token, "token_type": "bearer"}


    