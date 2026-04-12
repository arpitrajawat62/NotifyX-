from fastapi import FastAPI
from app.db.database import Base, engine
from app.api.routes import alerts, auth
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv


load_dotenv()

app = FastAPI()

Base.metadata.create_all(bind=engine)

#routes
app.include_router(alerts.router)
app.include_router(auth.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)




