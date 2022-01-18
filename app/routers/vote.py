from fastapi.exceptions import HTTPException
from fastapi.routing import APIRouter
from sqlalchemy.sql.expression import select
from sqlalchemy.sql.functions import mode
from .. import models, schemas
from fastapi import status, Depends
from sqlalchemy.orm.session import Session
from ..database import get_db
from ..oauth2 import get_current_user
from app import oauth2


router = APIRouter(
    prefix="/vote",
    tags=['Vote']
)


@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    check_post_quer = db.query(models.Post).filter(
        vote.post_id == models.Post.id)
    if not check_post_quer.first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f'post with id {vote.post_id} does not exists!')

    vote_query = db.query(models.Vote).filter(
        models.Vote.user_id == current_user.id, models.Vote.post_id == vote.post_id)
    found_vote = vote_query.first()
    if (vote.dir == 1):
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail=f'current_user: {current_user.id} has already vote on the post {vote.post_id}')
        new_vote = models.Vote(post_id=vote.post_id, user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message": "successfully added vote"}
    else:
        if not found_vote:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=f'Vote does not exist')

        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message": "successfully deleted vote"}
