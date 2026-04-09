from sqlmodel import Session
from database import engine
from models import *

def seed():
    with Session(engine) as session:
        client_a = Client(name="Client A", short_code="A")
        client_b = Client(name="Client B", short_code="B")

        agent = User(email="agent@test.com", name="Agent", role="agent")
        director = User(email="director@test.com", name="Director", role="director")

        session.add_all([client_a, client_b, agent, director])
        session.commit()

        assignment = UserClientAssignment(user_id=agent.id, client_id=client_a.id)
        session.add(assignment)

        for i in range(5):
            case = DenialCase(
                client_id=client_a.id if i < 3 else client_b.id,
                case_number=f"C-{i}",
                payer_name="Aetna",
                denied_amount=100 + i,
                status="new",
                priority=3
            )
            session.add(case)

        session.commit()

seed()
