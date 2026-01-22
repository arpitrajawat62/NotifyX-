from fastapi import FastAPI
from sqlalchemy import Engine
from app.db.database import Base, engine
from app.db import models
from app.api.routes import alerts 

app = FastAPI()


#routes
app.include_router(alerts.router)

Base.metadata.create_all(bind=engine)

