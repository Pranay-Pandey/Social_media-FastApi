from pyexpat import model
from .. import schemas, utils, models, oauth2
from fastapi import FastAPI, Response , status, HTTPException, Depends, APIRouter
from ..database import get_db
from sqlalchemy.orm import Session

from app import database

router = APIRouter(
    prefix = "/vote",
    tags= ['Vote']
)

@router.post('/' ,status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db: Session = Depends(database.get_db), current_user: int = Depends(oauth2.get_current_user)):

    if not db.query(models.Post).filter(models.Post.id==vote.post_id).first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'post with id {vote.post_id} does not exist')


    vote_query = db.query(models.Vote).filter(models.Vote.post_id==vote.post_id, models.Vote.user_id == current_user.id)
    found_post = vote_query.first()
    if (vote.dir==1):
        if found_post:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f'user {current_user.id} has already liked post {vote.post_id}')
        else:
            new_vote = models.Vote(post_id = vote.post_id, user_id = current_user.id)
            db.add(new_vote)
            db.commit()

            return {"message": "successfully added vote"}
    else:
        if not found_post:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Vote does not exist")

        vote_query.delete(synchronize_session=False)
        db.commit()

        return {"message": "Successfully deletd vote"}
