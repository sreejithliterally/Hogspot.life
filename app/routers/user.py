from fastapi import status, HTTPException,Depends, APIRouter
from sqlalchemy.orm import Session
import models, schemas, utils
from database import get_db
import random

router = APIRouter(
    prefix="/users",
    tags=['Users']
)

@router.post("/register", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(models.User).filter(models.User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    if user.password != user.confirm_password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Passwords do not match")

    hashed_password = utils.hash(user.password)
    new_user = models.User(
        name=user.name,
        email=user.email,
        password=hashed_password,
        date_of_birth=user.date_of_birth
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user





