from fastapi import status, HTTPException,Depends,APIRouter
from typing import List

from sqlalchemy.orm import Session
from sqlalchemy import func
import models, schemas, utils
from database import get_db
from datetime import datetime
from sqlalchemy.orm import joinedload

from oauth2 import get_current_user

router = APIRouter(
    prefix="/matches",
    tags=['match']
)

@router.get("/",status_code=status.HTTP_202_ACCEPTED,response_model=List[schemas.UserOut])
def match(current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    matches_as_user1 = db.query(models.Match).options(joinedload(models.Match.user2)).filter(models.Match.user1_id == current_user.id).all()
    matches_as_user2 = db.query(models.Match).options(joinedload(models.Match.user1)).filter(models.Match.user2_id == current_user.id).all()

    matched_users = [match.user2 for match in matches_as_user1] + [match.user1 for match in matches_as_user2]
    

    return matched_users