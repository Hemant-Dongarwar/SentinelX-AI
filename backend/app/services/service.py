from sqlalchemy.orm import Session

from app.models.alert import Alert


def create_alert(db: Session, alert, user_id):

    db_alert = Alert(
        title=alert.title,
        description=alert.description,
        severity=alert.severity,
        mitre=alert.mitre,
        user_id=user_id
    )

    db.add(db_alert)
    db.commit()
    db.refresh(db_alert)

    return db_alert


def get_alerts(db: Session):

    return db.query(Alert).all()