from sqlalchemy.orm import Session
from app.schemas.alert import CreateAlert
from app.db import models


def create_alert(alert_in: CreateAlert, db: Session):
    new_alert = models.Alert(
        user_id = alert_in.user_id,
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


