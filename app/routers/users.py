from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from app.database.db import get_session
from app.models.user import User, UserCreate, UserPublic
from app.utils.auth import get_password_hash

router = APIRouter()

@router.post(
    "/users/register/",
    response_model=UserPublic,
    status_code=status.HTTP_201_CREATED,
)
def create_user(user_create: UserCreate, session: Session = Depends(get_session)):
    existing_user = session.exec(
        select(User).where(User.username == user_create.username)
    ).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"User {user_create.username} already exists",
        )

    existing_email = session.exec(
        select(User).where(User.email == user_create.email)
    ).first()
    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"E-mail {user_create.email} already used",
        )

    hashed_password = get_password_hash(user_create.password)

    user_data = user_create.model_dump(exclude={"password"})
    user = User(**user_data, hashed_password=hashed_password)

    session.add(user)
    session.commit()
    session.refresh(user)
    return user

@router.get("/users/", response_model=List[UserPublic])
def get_users(session: Session = Depends(get_session)):
    users = session.exec(select(User)).all()
    return users

@router.get("/users/{user_id}", response_model=UserPublic)
def get_user(user_id: int, session: Session = Depends(get_session)):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user