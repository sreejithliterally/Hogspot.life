from fastapi import status, HTTPException,Depends, APIRouter,UploadFile, File
from typing import List
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
import models, schemas, utils
from database import get_db
import random
from oauth2 import get_current_user
import boto3
from botocore.exceptions import NoCredentialsError
from config import settings

AWS_SERVER_PUBLIC_KEY = settings.AWS_SERVER_PUBLIC_KEY
AWS_SERVER_SECRET_KEY = settings.AWS_SERVER_SECRET_KEY

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


@router.put("/complete_profile", response_model=schemas.UserOut)
def complete_profile(
    profile_data: schemas.CompleteProfile,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    user = db.query(models.User).filter(models.User.id == current_user.id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if profile_data.bio is not None:
        user.bio = profile_data.bio
    if profile_data.gender is not None:
        user.gender = profile_data.gender

    db.commit()
    db.refresh(user)
    
    return user

def upload_image_to_s3(image, bucket_name):
    s3 = boto3.client('s3')
    try:
        s3.upload_fileobj(image.file, bucket_name, image.filename)
        image_url = f"https://{bucket_name}.s3.amazonaws.com/{image.filename}"
        return image_url
    except NoCredentialsError:
        return None
    
@router.post("/upload_image", response_model=schemas.UserImageOut)
def upload_image(
    file: UploadFile = File(...),
    priority: int = 0,  # Accept priority as a parameter
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    user = db.query(models.User).filter(models.User.id == current_user.id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    file_url = upload_image_to_s3(file, user.id, 'travelactivity')

    user_image = models.UserImage(
        user_id=user.id,
        image_url=file_url,
        priority=priority  # Set priority
    )
    db.add(user_image)
    db.commit()
    db.refresh(user_image)

    return user_image

@router.put("/update_image_priority/{image_id}", response_model=schemas.UserImageOut)
def update_image_priority(
    image_id: int,
    priority: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    user_image = db.query(models.UserImage).filter(models.UserImage.id == image_id, models.UserImage.user_id == current_user.id).first()
    if not user_image:
        raise HTTPException(status_code=404, detail="Image not found or not authorized")

    user_image.priority = priority
    db.commit()
    db.refresh(user_image)

    return user_image

@router.get("/profile_images", response_model=List[schemas.UserImageOut])
def get_profile_images(current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    images = db.query(models.UserImage).filter(models.UserImage.user_id == current_user.id).order_by(models.UserImage.priority).all()
    return images

