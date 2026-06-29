from app.services.dashboard_service import get_dashboard_stats
from app.schemas.dashboard import DashboardResponse

from app.services.ai_service import analyze_alert
from app.schemas.analysis import AIAnalysisResponse

from fastapi import FastAPI, Depends, HTTPException
from fastapi.openapi.utils import get_openapi
from sqlalchemy.orm import Session

from app.database.database import engine, get_db
from app.database.base import Base

from app.schemas.user import UserCreate
from app.schemas.login import LoginRequest
from app.schemas.alert import AlertCreate, AlertResponse, AlertUpdate

from app.services.user_service import create_user
from app.services.auth_service import authenticate_user

from app.services.alert_service import (
    create_alert,
    get_alerts,
    get_user_alerts,
    update_alert,
    delete_alert
)

from app.models.user import User

from app.utils.security import create_access_token
from app.core.auth import get_current_user


# Create Database Tables
Base.metadata.create_all(bind=engine)


# FastAPI App
app = FastAPI(
    title="SentinelX AI",
    description="AI Powered SOC Analyst",
    version="1.0.0"
)


# Root
@app.get("/")
def root():
    return {
        "message": "Welcome to SentinelX AI 🚀"
    }


# Health Check
@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


# Register
@app.post("/register")
def register(
    user: UserCreate,
    db: Session = Depends(get_db)
):
    new_user = create_user(
        db=db,
        username=user.username,
        email=user.email,
        password=user.password
    )

    return {
        "message": "User registered successfully",
        "id": new_user.id,
        "username": new_user.username,
        "email": new_user.email
    }


# Login
@app.post("/login")
def login(
    request: LoginRequest,
    db: Session = Depends(get_db)
):
    user = authenticate_user(
        db,
        request.username,
        request.password
    )

    if not user:
        return {
            "message": "Invalid username or password"
        }

    access_token = create_access_token(
        {
            "sub": user.username
        }
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


# Current User
@app.get("/me")
def get_me(
    current_user: User = Depends(get_current_user)
):
    return {
        "id": current_user.id,
        "username": current_user.username,
        "email": current_user.email
    }


# Create Alert
@app.post("/alerts", response_model=AlertResponse)
def create_new_alert(
    alert: AlertCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return create_alert(
        db,
        alert,
        current_user.id
    )


# Get Alerts
@app.get("/alerts", response_model=list[AlertResponse])
def list_alerts(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_alerts(db)

@app.put("/alerts/{alert_id}", response_model=AlertResponse)
def update_existing_alert(
    alert_id: int,
    alert_update: AlertUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    updated_alert = update_alert(
        db=db,
        alert_id=alert_id,
        alert_update=alert_update,
        user_id=current_user.id
    )

    if updated_alert is None:
        raise HTTPException(
            status_code=404,
            detail="Alert not found"
        )

    return updated_alert

@app.get("/my-alerts", response_model=list[AlertResponse])
def my_alerts(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_user_alerts(db, current_user.id)

@app.get("/analyze/{mitre_id}", response_model=AIAnalysisResponse)
def analyze(mitre_id: str):
    return analyze_alert(mitre_id)

@app.get("/dashboard", response_model=DashboardResponse)
def dashboard(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_dashboard_stats(db)

@app.delete("/alerts/{alert_id}", response_model=AlertResponse)
def delete_existing_alert(
    alert_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    deleted_alert = delete_alert(
        db=db,
        alert_id=alert_id,
        user_id=current_user.id
    )

    if deleted_alert is None:
        raise HTTPException(
            status_code=404,
            detail="Alert not found"
        )

    return deleted_alert


# Swagger JWT Support
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )

    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT"
        }
    }

    for path, path_item in openapi_schema["paths"].items():

        if path in [
            "/me",
            "/alerts",
            "/my-alerts",
            "/dashboard",
            "/alerts/{alert_id}"
        ]:
            for operation in path_item.values():
                operation["security"] = [
                    {
                        "BearerAuth": []
                    }
                ]   

    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi