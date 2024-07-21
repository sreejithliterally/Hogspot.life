from fastapi import status, HTTPException,Depends,APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import func
import models, schemas, utils
from database import get_db
from datetime import datetime

from oauth2 import get_current_user

router = APIRouter(
    prefix="/swipe",
    tags=['swipe']
)

@router.post("/",status_code=status.HTTP_201_CREATED)
def swipe(swipe_data:schemas.Swipe, current_user:models.User = Depends(get_current_user),db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == current_user.id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {current_user.id} not found")
    
    swiped_user  = db.query(models.User).filter_by(id=swipe_data.swiped_user_id).first()
    if not swiped_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {swipe_data.swiped_user_id} not found")

    swipe = models.Swipe(
        user_id = current_user.id,
        swiped_user_id = swipe_data.swiped_user_id,
        swipe_type = swipe_data.swipe_type,
        created_at = datetime.now()
    )

    db.add(swipe)
    db.commit()
    
    if swipe_data.swipe_type =='right':
        opposite_swipe = db.query(models.Swipe).filter_by(
            user_id = swipe_data.swiped_user_id,
            swiped_user_id = current_user.id,
            swipe_type = "right"
        ).first()

        if opposite_swipe:
            match = models.Match(
                user1_id=min(current_user.id, swiped_user.id),
                user2_id=max(current_user.id, swiped_user.id),
                created_at=datetime.now()
            )
            db.add(match)
            db.commit()
            return {"its a match"}
    
    return {"detail": "Swipe recorded successfully"}
