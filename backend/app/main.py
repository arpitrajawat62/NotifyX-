from fastapi import FastAPI
from sqlalchemy import Engine
from app.api.router import api_router
from app.db.database import Base, engine
from app.db import models

app = FastAPI()



Base.metadata.create_all(bind=engine)


app.include_router(api_router)