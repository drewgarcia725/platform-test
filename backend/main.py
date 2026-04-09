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
