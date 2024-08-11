from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas, utils
from datetime import datetime
from app.database import get_db
from app.oauth2 import get_current_user


from shapely.geometry import Point, Polygon


router = APIRouter(
    prefix="/hotspot",
    tags=['hotspot']
)

@router.post("/update_location")
def update_location(location: schemas.Location, current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == current_user.id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.latitude = location.latitude
    user.longitude = location.longitude
    db.commit()

    # Find active hotspots
    active_hotspots = db.query(models.Hotspot).filter(models.Hotspot.status == True).all()

    # Create a Point for the user's location (longitude, latitude)
    user_location = Point(location.longitude, location.latitude)

    user_in_hotspots = []
    for hotspot in active_hotspots:
        # Convert the coordinates to a list of tuples
        coords = [(float(coord[0]), float(coord[1])) for coord in hotspot.coordinates]
        
        # Convert hotspot coordinates into a Polygon
        hotspot_polygon = Polygon(coords)
        
        if hotspot_polygon.contains(user_location):
            user_in_hotspots.append(hotspot)

    # Update or create UserHotspot entries for the current user
    for hotspot in user_in_hotspots:
        user_hotspot = db.query(models.UserHotspot).filter_by(user_id=user.id, hotspot_id=hotspot.id).first()
        if user_hotspot:
            user_hotspot.last_seen_at = datetime.utcnow()
        else:
            user_hotspot = models.UserHotspot(
                user_id=user.id, hotspot_id=hotspot.id, entered_at=datetime.utcnow(), last_seen_at=datetime.utcnow()
            )
            db.add(user_hotspot)
    
    db.commit()

    # Remove user from hotspots they are no longer in
    db.query(models.UserHotspot).filter(
        models.UserHotspot.user_id == user.id,
        models.UserHotspot.hotspot_id.notin_([hotspot.id for hotspot in user_in_hotspots])
    ).delete(synchronize_session='fetch')
    
    db.commit()

    return {"status": "success", "message": "Location updated successfully"}
