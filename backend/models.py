from typing import Optional
from sqlmodel import SQLModel, Field
from uuid import uuid4, UUID
from datetime import datetime

class Client(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    name: str
    short_code: str

class User(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    email: str
    name: str
    role: str  # agent | director

class UserClientAssignment(SQLModel, table=True):
    user_id: UUID = Field(foreign_key="user.id", primary_key=True)
    client_id: UUID = Field(foreign_key="client.id", primary_key=True)

class DenialCase(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    client_id: UUID = Field(foreign_key="client.id")
    case_number: str
    payer_name: str
    denied_amount: float
    status: str  # new | in_review | approved | closed
    priority: int
    created_at: datetime = Field(default_factory=datetime.utcnow)

