from fastapi import FastAPI
from . import models
from .database import engin
from .routers import post, user, auth

models.Base.metadata.create_all(bind=engin)

app = FastAPI()

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
