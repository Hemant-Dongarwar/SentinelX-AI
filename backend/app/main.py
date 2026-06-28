from app.services.ai_service import analyze_alert
from app.schemas.analysis import AIAnalysisResponse

from fastapi import FastAPI, Depends
from fastapi.openapi.utils import get_openapi
from sqlalchemy.orm import Session

from app.database.database import engine, get_db
from app.database.base import Base

from app.schemas.user import UserCreate
from app.schemas.login import LoginRequest
from app.schemas.alert import AlertCreate, AlertResponse

from app.services.user_service import create_user
from app.services.auth_service import authenticate_user

from app.services.alert_service import (
    create_alert,
    get_alerts,
    get_user_alerts
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

@app.get("/my-alerts", response_model=list[AlertResponse])
def my_alerts(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_user_alerts(db, current_user.id)

@app.get("/analyze/{mitre_id}", response_model=AIAnalysisResponse)
def analyze(mitre_id: str):
    return analyze_alert(mitre_id)


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

    for path in openapi_schema["paths"].values():
        for operation in path.values():
           if operation.get("operationId") in [
                "get_me_me_get",
                "create_new_alert_alerts_post",
                "list_alerts_alerts_get",
                "my_alerts_my_alerts_get"
            ]:
                operation["security"] = [
                    {
                        "BearerAuth": []
                    }
                ]

    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi