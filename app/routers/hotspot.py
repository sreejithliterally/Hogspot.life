from fastapi import status, HTTPException,Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import func
from app import models, schemas, utils
from app.database import get_db
from datetime import datetime, date
import random
from shapely.geometry import Point, Polygon
from app.oauth2 import get_current_user
import re
router = APIRouter(
    prefix="/hotspot",
    tags=['hotspot']
)

@router.post("/new", status_code=status.HTTP_201_CREATED, response_model=schemas.HotspotOut)
def register(hotspot: schemas.HotspotCreate, db: Session = Depends(get_db)):
    # Create a list of tuples from the coordinates
    coordinates = [(coord[0], coord[1]) for coord in hotspot.coordinates]

    new_spot = models.Hotspot(
        name=hotspot.name,
        description=hotspot.description,
        coordinates=coordinates,
        status=hotspot.status
    )
    db.add(new_spot)
    db.commit()
    db.refresh(new_spot)
    
    return new_spot




@router.post("/start_swiping")
def start_swiping(location: schemas.Location, current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == current_user.id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.latitude = location.latitude
    user.longitude = location.longitude
    db.commit()

    # Find active hotspots
    active_hotspots = db.query(models.Hotspot).filter(models.Hotspot.status == True).all()

    # Create a Point for the user's location (longitude, latitude)
    user_location = Point(location.latitude, location.longitude)

    user_in_hotspots = []
    for hotspot in active_hotspots:
        # Convert the coordinates to a list of tuples
        coords = [(float(coord[0]), float(coord[1])) for coord in hotspot.coordinates]
        
        # Convert hotspot coordinates into a Polygon
        hotspot_polygon = Polygon(coords)
        print(hotspot_polygon)
        if hotspot_polygon.contains(user_location):
            user_in_hotspots.append(hotspot)

    if user_in_hotspots:
        for hotspot in user_in_hotspots:
            user_hotspot = db.query(models.UserHotspot).filter_by(user_id=user.id, hotspot_id=hotspot.id).first()
            if user_hotspot:
                user_hotspot.last_seen_at = datetime.utcnow()
            else:
                user_hotspot = models.UserHotspot(
                    user_id=user.id, hotspot_id=hotspot.id, entered_at=datetime.utcnow()
                )
                db.add(user_hotspot)
        
        db.commit()

        hotspot_users = db.query(models.User).join(models.UserHotspot).filter(
            models.UserHotspot.hotspot_id.in_([hotspot.id for hotspot in user_in_hotspots]),
            models.User.id != user.id  # Exclude the current user
        ).all()
        
        # Prepare response data
        response_data = {
            "status": "success",
            "message": "User is within an active hotspot",
            "hotspots": [
                {"id": hotspot.id, "name": hotspot.name, "description": hotspot.description} 
                for hotspot in user_in_hotspots
            ],
            "other_users": [
                {
                    "id": u.id,
                    "name": u.name,
                    "bio": u.bio,
                    "age": calculate_age(u.date_of_birth),
                    "images": [
                        {"image_url": img.image_url, "priority": img.priority}
                        for img in u.images
                    ]
                }
                for u in hotspot_users
            ]
        }

        return response_data
    else:
        return {
            "status": "failure",
            "message": "User is not within any active hotspots"
        }
    
def calculate_age(dob: date) -> int:
    today = datetime.today().date()  
    age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
    return age