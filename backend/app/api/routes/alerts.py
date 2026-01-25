from fastapi import APIRouter
from app.schemas.alert import CreateAlert, AlertResponse
from app.db.database import db_dependency
from app.services.alert_service import create_alert



router = APIRouter(
    prefix="/alerts",
    tags=["alerts"]
)

@router.post("/", response_model=AlertResponse)
def create_new_alert(alert_in: CreateAlert, db: db_dependency):
    alert = create_alert(db=db, alert_in=alert_in)
    return alert