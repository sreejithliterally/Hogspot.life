from fastapi import status, HTTPException,Depends, APIRouter
from sqlalchemy.orm import Session
import models, otp as otp
from database import get_db
from datetime import datetime, timedelta


router = APIRouter(
    prefix="/verify",
    tags=['Verification']
)

@router.post("/verify-email", status_code=status.HTTP_200_OK)
def verify_email(email: str, db: Session = Depends(get_db)):
    existing_user = db.query(models.User).filter(models.User.email == email).first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    
    otp_code = otp.generate_otp()
    expiration_time = datetime.utcnow() + timedelta(minutes=10)  # OTP valid for 10 minutes
    otp_entry = models.OTP(email=email, otp_code=otp_code, expiration_time=expiration_time)
    db.add(otp_entry)
    db.commit()
    
    otp.send_otp(email, otp_code)
    
    return {"msg": "OTP sent to your email."}

@router.post("/verify-otp", status_code=status.HTTP_200_OK)
def verify_otp(email: str, otp_code: str, db: Session = Depends(get_db)):
    otp_entry = db.query(models.OTP).filter(models.OTP.email == email, models.OTP.otp_code == otp_code).first()
    if not otp_entry or otp_entry.expiration_time< datetime.utcnow():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid or expired OTP")

    db.delete(otp_entry)
    db.commit()
    
    return {"msg": "Email verified successfully."}

