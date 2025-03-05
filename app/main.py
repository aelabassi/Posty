"""
Main application
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from . import db_storage
from app.db_storage import engine
from .routers import user, post, auth, vote

load_dotenv()
db_storage.Base.metadata.create_all(bind=engine)


app = FastAPI()
# CORS
# origins = ["https://google.com"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# include post router
app.include_router(user.router)

# include user router
app.include_router(post.router)

# include vote router
app.include_router(vote.router)

# include auth router
app.include_router(auth.router)

@app.get("/")
async def root():
    return {"message": "Hello World"}
