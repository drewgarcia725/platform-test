from fastapi import FastAPI, Depends, Header, HTTPException
from sqlmodel import Session, select
from database import get_session, init_db
from uuid import UUID
from models import *
from typing import Optional

app = FastAPI()

@app.on_event("startup")
def on_startup():
    init_db()



def get_current_user(
    x_user_id: str = Header(...),
    session: Session = Depends(get_session)
):
    try:
        user_id = UUID(x_user_id)  # 🔥 convert string → UUID
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid user ID format")

    user = session.get(User, user_id)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user


def get_user(session, user_id):
    return session.get(User, user_id)

def get_user_client_ids(session, user_id: UUID):
    results = session.exec(
        select(UserClientAssignment.client_id).where(
            UserClientAssignment.user_id == user_id
        )
    ).all()

    return results

def check_access(user, client_id, allowed_clients):
    if user.role == "director":
        return True
    return client_id in allowed_clients


def test_agent_cannot_access_other_client_case():
    # pseudo-code
    response = client.get("/api/cases/{case_from_other_client}",
        headers={"X-User-Id": agent_id})

    assert response.status_code == 403

@app.get("/api/cases")
def list_cases(
    limit: int = 20,
    offset: int = 0,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user)
):
    query = select(DenialCase)

    if user.role == "agent":
        allowed_clients = get_user_client_ids(session, user.id)

        if not allowed_clients:
            return []

        query = query.where(DenialCase.client_id.in_(allowed_clients))

    return session.exec(query.offset(offset).limit(limit)).all()

@app.get("/api/cases/{case_id}")
def get_case(case_id: str, session: Session = Depends(get_session), user: User = Depends(get_user)):
    case = session.get(DenialCase, case_id)
    if not case:
        raise HTTPException(status_code=404)
    if user.role == "agent" and case.client_id not in [uc.client_id for uc in user.assignments]:
        raise HTTPException(status_code=403)
    return case

@app.post("/api/cases")
def create_case(case: DenialCase, session: Session = Depends(get_session), user: User = Depends(get_user)):
    if user.role == "agent" and case.client_id not in [uc.client_id for uc in user.assignments]:
        raise HTTPException(status_code=403)
    session.add(case)
    session.commit()
    session.refresh(case)
    return case
