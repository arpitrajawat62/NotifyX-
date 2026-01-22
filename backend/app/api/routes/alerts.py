from fastapi import APIRouter, Depends
from app.schemas.alert import CreateAlert
from app.db.models import Alert
from app.schemas import user
from app.services import alert_service
from app.db.models import Alert
from app.schemas.alert import CreateAlert
from app.db.database import db_dependency



router = APIRouter(
    prefix="/alerts",
    tags=["alerts"]
)

@router.post("/")
def create_alert(alert_in: CreateAlert, db: db_dependency):
    
    alert = alert = Alert(
        **alert_in.dict(),
        user_id= 1
    )

    db.add(alert)
    db.commit()
    db.refresh(alert)

    return alert