from datetime import datetime, timezone
from sqlmodel import SQLModel, Field, Relationship

class UserBase(SQLModel):
    username: str = Field(unique=True, index=True)
    email: str = Field(unique=True, index=True)
    is_active: bool = Field(default=True)

class User(UserBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    hashed_password: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    # Relationships
    posts: list = Relationship(back_populates="author")
    events: list = Relationship(back_populates="author")

class UserCreate(SQLModel):
    username: str
    email: str
    password: str

class UserPublic(UserBase):
    id: int
    created_at: datetime

class UserUpdate(SQLModel):
    username: str | None = None
    email: str | None = None
    password: str | None = None
    is_active: bool | None = None

# AUTHENTIFICATION
class UserLogin(SQLModel):
    username: str
    password: str