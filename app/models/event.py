from datetime import datetime
from typing import TYPE_CHECKING, Optional
from sqlmodel import Field, SQLModel, Relationship

class EventBase(SQLModel):
    title: str
    description: str
    location: str
    end: datetime
    start: datetime
    all_day: bool = Field(default=False)

class Event(EventBase, Table=True):
    id: int | None = Field(default=None, primary_key=True)

    # Foreign Keys
    author_id: int = Field(foreign_key="user.id")

    # Relationships
    author: Optional = Relationship(back_populates="posts")

class EventCreate(EventBase):
    pass

class EventPublic(Event):
    id: int

class EventUpdate(EventBase):
    title: str | None = None
    description: str | None = None
    location: str | None = None
    end: datetime | None = None
    all_day: bool | None = None