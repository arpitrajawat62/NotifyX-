from fastapi import FastAPI
from app.db.database import Base, engine
from app.api.routes import alerts, auth
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()


#routes
app.include_router(alerts.router)
app.include_router(auth.router)

Base.metadata.create_all(bind=engine)

