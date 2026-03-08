from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.schemas.alert import CreateAlert
from app.db.models import Alert




def create_alert(alert_in: CreateAlert, db: Session, current_user_id: int):

    if not alert_in.query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty")
    
    existing_alert = db.query(Alert).filter(Alert.user_id == current_user_id, Alert.query == alert_in.query).first()
    if existing_alert:
        raise HTTPException(status_code=409, detail="Alert already exists")
    
    new_alert = Alert(
        user_id = current_user_id,
        query = alert_in.query,
        frequency = "daily",
        source = "rss",
        last_checked_at = None,
        is_active = True
    )
    
    db.add(new_alert)
    db.commit()
    db.refresh(new_alert)
    return new_alert

def get_all_alerts(db: Session, current_user_id: int):
    return db.query(Alert).filter(Alert.user_id == current_user_id).all()
    

def get_alert_by_id(db: Session, alert_id: int, current_user_id: int):
    return db.query(Alert).filter(Alert.id == alert_id, Alert.user_id == current_user_id).first()
    

def delete_alert(db: Session, alert_id: int, current_user_id: int):
    alert = db.query(Alert).filter(Alert.id == alert_id, Alert.user_id == current_user_id).first()   

    if not alert:
        return None
    
    db.delete(alert)
    db.commit()
    
    return alert

     
