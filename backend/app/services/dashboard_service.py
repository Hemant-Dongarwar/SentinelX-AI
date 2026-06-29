from sqlalchemy.orm import Session
from app.models.alert import Alert


def get_dashboard_stats(db: Session):

    alerts = db.query(Alert).all()

    print("========== DASHBOARD DEBUG ==========")
    print("Total Alerts:", len(alerts))

    for alert in alerts:
        print(alert.id, alert.title, alert.severity, alert.status)

    total_alerts = db.query(Alert).count()

    open_alerts = db.query(Alert).filter(
        Alert.status == "Open"
    ).count()

    closed_alerts = db.query(Alert).filter(
        Alert.status == "Closed"
    ).count()

    critical_alerts = db.query(Alert).filter(
        Alert.severity == "Critical"
    ).count()

    high_alerts = db.query(Alert).filter(
        Alert.severity == "High"
    ).count()

    medium_alerts = db.query(Alert).filter(
        Alert.severity == "Medium"
    ).count()

    low_alerts = db.query(Alert).filter(
        Alert.severity == "Low"
    ).count()

    return {
        "total_alerts": total_alerts,
        "open_alerts": open_alerts,
        "closed_alerts": closed_alerts,
        "critical_alerts": critical_alerts,
        "high_alerts": high_alerts,
        "medium_alerts": medium_alerts,
        "low_alerts": low_alerts
    }