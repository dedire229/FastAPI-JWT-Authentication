from sqlmodel import Field, Session, SQLModel
from uuid import uuid4, UUID

class User(SQLModel, table=True):
    """User model."""
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    username: str = Field(index=True, unique=True)
    email: str = Field(index=True)
    hashed_pwd: str
