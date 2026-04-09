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


def get_user(session, user_id):
    return session.get(User, user_id)

def get_user_client_ids(session, user_id):
    assignments = session.query(UserClientAssignment).filter_by(user_id=user_id).all()
    return [a.client_id for a in assignments]

def check_access(user, client_id, allowed_clients):
    if user.role == "director":
        return True
    return client_id in allowed_clients
