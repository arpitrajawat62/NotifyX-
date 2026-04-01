from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from app.schemas.alert import CreateAlert, AlertResponse
from app.db.database import db_dependency
from app.db.models import User
from app.services.alert_service import (
    create_alert,
    get_all_alerts,
    get_alert_by_id,
    delete_alert
)
from app.api.routes.auth import get_current_user
from fastapi import BackgroundTasks
from app.services.email_sender import send_email


CurrentUser = Annotated[dict, Depends(get_current_user)]


router = APIRouter(
    prefix="/alerts",
    tags=["alerts"]
)

@router.post("/", response_model=AlertResponse, status_code=201)
def create_new_alert(alert_in: CreateAlert, db: db_dependency, current_user: CurrentUser, background_tasks: BackgroundTasks):
    alert = create_alert(db=db, alert_in=alert_in, current_user_id=current_user["id"])

    user = db.query(User).filter(User.id == current_user["id"]).first()

    if user:
        background_tasks.add_task(
            send_email,
            user.email,
            "Alert Created",
            f"Your alert '{alert.query}' has been created successfully."
        )
    return alert


@router.get("/", response_model=list[AlertResponse])
def get_user_alerts(db :db_dependency, current_user: CurrentUser):
     return get_all_alerts(db, current_user["id"])
    

@router.get("/{alert_id}", response_model=AlertResponse)
def get_single_alert(alert_id: int, db: db_dependency,current_user: CurrentUser):
     
     alert = get_alert_by_id(db, alert_id, current_user["id"])
     if not alert:
        raise HTTPException(status_code=404, detail='Alert not found')
     return alert


@router.delete("/{alert_id}", response_model=AlertResponse)
def delete_alert_route(alert_id: int, db: db_dependency, current_user: CurrentUser):
    success = delete_alert(db, alert_id, current_user["id"])
    if not success:
            raise HTTPException(status_code=404, detail="Alert not found")
    return success

