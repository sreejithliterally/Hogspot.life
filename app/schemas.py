from pydantic import BaseModel, EmailStr
from datetime import datetime,time as Time, date
from typing import Dict, Optional, Union, Tuple
from enum import Enum
from fastapi import UploadFile
from fastapi import Form, File
from typing import List

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    confirm_password: str
    date_of_birth: date
    

class UserOut(BaseModel):
    id: int
    name: str
    email: EmailStr
    date_of_birth: date
    is_verified: bool

    class Config:
        orm_mode = True

class UserImageCreate(BaseModel):
    image_url: str


class UserImageOut(BaseModel):
    id: int
    image_url: str
    priority: int

    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    email : EmailStr
    password : str

class EducationLevel(str, Enum):
    school = "school"
    college = "college"

class SmokingHabit(str, Enum):
    occasionally = "occasionally"
    never = "never"
    socially = "socially"

class DrinkingHabit(str, Enum):
    occasionally = "occasionally"
    never = "never"
    socially = "socially"

class WorkoutHabit(str, Enum):
    daily = "daily"
    never = "never"
    sometimes = "sometimes"

class Interest(str, Enum):
    football = "football"
    tennis = "tennis"
    cricket = "cricket"
    other_sports = "other_sports"
    books = "books"
    arts = "arts"
    rides = "rides"
    trekking = "trekking"
    swimming = "swimming"
    movies = "movies"
    music = "music"
    coding = "coding"
    others = "others"

class CompleteProfile(BaseModel):
    bio: Optional[str] = None
    gender: Optional[str] = None
    education_level: Optional[EducationLevel] = None
    college_name: Optional[str] = None
    profession: Optional[str] = None
    company: Optional[str] = None
    height_cm: Optional[float] = None
    smoking: Optional[SmokingHabit] = None
    drinking: Optional[DrinkingHabit] = None
    workout: Optional[WorkoutHabit] = None
    interests: Optional[Interest] = None





class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: int



class HotspotCreate(BaseModel):
    name: str
    description:str
    coordinates: List[Tuple[float, float]]
    status: bool 

class HotspotOut(BaseModel):
    id: int
    name: str
    description:str
    coordinates: List[Tuple[float, float]]
    status: bool 

class Location(BaseModel):
    latitude: float
    longitude: float


class Swipe(BaseModel):
    swiped_user_id: int
    swipe_type: str  # 'right' or 'left'

    class Config:
        orm_mode = True