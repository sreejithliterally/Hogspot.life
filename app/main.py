from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app import models
from app.database import engine
from app.routers import user, userauth,verify_email, hotspot, update_userlocation, swipe,getmatches, chat
from dotenv import load_dotenv


load_dotenv()
app = FastAPI()



origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


models.Base.metadata.create_all(bind=engine)

app.include_router(user.router)
app.include_router(userauth.router)
app.include_router(verify_email.router)
app.include_router(hotspot.router)
app.include_router(update_userlocation.router)
app.include_router(swipe.router)
app.include_router(getmatches.router)
app.include_router(chat.router)



@app.get("/")
async def root():
    return {"message": "Hello World"}
