from typing import Optional
from sqlmodel import Field, SQLModel, Relationship
from datetime import datetime, timezone

class PostBase(SQLModel):
    title: str
    content: str
    published: bool | None = Field(default=False)


class Post(PostBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column_kwargs={"onupdate": lambda: datetime.now(timezone.utc)}
    )

    # Foreign Keys
    author_id: int = Field(foreign_key="user.id")

    # Relationships
    author: Optional = Relationship(back_populates="posts")


class PostCreate(PostBase):
    pass


class PostPublic(Post):
    id: int


class PostUpdate(PostBase):
    title: str | None = None
    content: str | None = None
    published: bool | None = None

class PostWithAuthor(PostPublic):
    author: "User"