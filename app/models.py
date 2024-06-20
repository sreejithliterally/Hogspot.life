from sqlalchemy import Column, Integer, String, Float, TIMESTAMP, func, Text, ForeignKey, DateTime, Boolean, Date, ARRAY
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from geoalchemy2 import Geography

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
        
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    latitude = Column(Float, nullable=True)  
    longitude = Column(Float, nullable=True)  
    radius = Column(Float, default=500.0)  
    date_of_birth = Column(Date, nullable=False)
    bio = Column(Text, nullable=True)
    gender = Column(String, nullable=True)
    
    is_verified = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    images = relationship("UserImage", back_populates="user")
    hotspots = relationship("UserHotspot", back_populates="user")

class UserImage(Base):
    __tablename__ = 'user_images'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    image_url = Column(String, nullable=False)
    priority = Column(Integer, default=0)  # New field for priority
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="images")


class OTP(Base):
    __tablename__ = 'otps'

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, index=True, nullable=False)  # Store email instead of user_id
    otp_code = Column(String, nullable=False)
    expiration_time = Column(DateTime, nullable=False)

class Hotspot(Base):
    __tablename__ = 'hotspots'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    coordinates = Column(ARRAY(Float))  
    description = Column(Text, nullable=True)
    radius = Column(Float, nullable=True, default=500.0)
    status = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    users = relationship("UserHotspot", back_populates="hotspot")

class UserHotspot(Base):
    __tablename__ = 'user_hotspots'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    hotspot_id = Column(Integer, ForeignKey('hotspots.id'), nullable=False)
    entered_at = Column(DateTime(timezone=True), server_default=func.now())
    last_seen_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    user = relationship("User", back_populates="hotspots")
    hotspot = relationship("Hotspot", back_populates="users")
