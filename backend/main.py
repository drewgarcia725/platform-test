from fastapi import FastAPI, Depends, Header, HTTPException
from sqlmodel import Session, select
from database import get_session, init_db
from models import *
from typing import Optional

app = FastAPI()

@app.on_event("startup")
def on_startup():
    init_db()

def get_current_user(x_user_id: str = Header(...), session: Session = Depends(get_session)):
    user = session.get(User, x_user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user



def get_user(session, user_id):
    return session.get(User, user_id)

def get_user_client_ids(session, user_id):
    assignments = session.exec(
        select(UserClientAssignment).where(
            UserClientAssignment.user_id == user_id
        )
    ).all()
    return [a.client_id for a in assignments]

def check_access(user, client_id, allowed_clients):
    if user.role == "director":
        return True
    return client_id in allowed_clients


