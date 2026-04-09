from sqlmodel import Session
from database import engine
from models import *
from datetime import datetime
import uuid

def seed():
    with Session(engine) as session:
        # Create clients
        client_a = Client(id=str(uuid.uuid4()), name="Client A", short_code="A")
        client_b = Client(id=str(uuid.uuid4()), name="Client B", short_code="B")

        # Create users
        agent = User(id=str(uuid.uuid4()), email="agent@test.com", name="Agent", role="agent")
        director = User(id=str(uuid.uuid4()), email="director@test.com", name="Director", role="director")

        session.add_all([client_a, client_b, agent, director])
        session.commit()

        # Assign agent to Client A
        assignment = UserClientAssignment(user_id=agent.id, client_id=client_a.id)
        session.add(assignment)

        # Create 5 denial cases
        for i in range(5):
            case = DenialCase(
                id=str(uuid.uuid4()),
                client_id=client_a.id if i < 3 else client_b.id,
                case_number=f"C-{i}",
                payer_name="Aetna",
                denied_amount=100 + i,
                status="new",
                priority=3,
                created_at=datetime.utcnow()
            )
            session.add(case)

        session.commit()
        print("Seed complete!")
        print("Agent ID:", agent.id)
        print("Director ID:", director.id)
        print("Client A ID:", client_a.id)
        print("Client B ID:", client_b.id)

if __name__ == "__main__":
    seed()
