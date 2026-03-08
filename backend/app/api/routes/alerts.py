from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from app.schemas.alert import CreateAlert, AlertResponse
from app.db.database import db_dependency
from app.services.alert_service import (
    create_alert,
    get_all_alerts,
    get_alert_by_id,
    delete_alert
)
from app.api.routes.auth import get_current_user


user_dependency = Annotated[dict, Depends(get_current_user)]

router = APIRouter(
    prefix="/alerts",
    tags=["alerts"]
)

@router.post("/", response_model=AlertResponse, status_code=201)
def create_new_alert(alert_in: CreateAlert, db: db_dependency, user: user_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    return create_alert(db=db, alert_in=alert_in, current_user_id=user["id"])


@router.get("/", response_model=list[AlertResponse])
def get_alerts(db :db_dependency, user: user_dependency):
     if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
     return get_all_alerts(db, user["id"])
    

@router.get("/{alert_id}", response_model=AlertResponse)
def get_alert(alert_id: int, db: db_dependency, user: user_dependency):
     
     alert = get_alert_by_id(db, alert_id, user["id"])
     if not alert:
        raise HTTPException(status_code=404, detail='Alert not found')
     return alert


@router.delete("/{alert_id}", response_model=AlertResponse)
def delete_alert_route(alert_id: int, db: db_dependency, user: user_dependency):
    deleted_alert = delete_alert(db, alert_id, user["id"])
    if not deleted_alert:
            raise HTTPException(status_code=404, detail="Alert not found")
    return deleted_alert

# @router.put("/{alert_id}", response_model=AlertResponse)
# def update_alert_route(alert_id: int, alert_in: updateAlert, db:db_dependency):
#     update_alert = update_alert(db, alert_id, alert_in)
#     return update_alert