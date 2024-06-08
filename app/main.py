from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import models
from database import engine
from routers import user, userauth, verify_email, hotspot
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





@app.get("/")
async def root():
    return {"message": "Hello World"}
