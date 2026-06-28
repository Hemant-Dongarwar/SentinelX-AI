from sqlalchemy.orm import Session

from app.models.user import User
from app.utils.security import hash_password


def create_user(db: Session, username: str, email: str, password: str):
    hashed = hash_password(password)

    user = User(
        username=username,
        email=email,
        password=hashed
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user