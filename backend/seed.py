from sqlmodel import Session
from database import engine
from models import Client, User, UserClientAssignment, DenialCase
from datetime import datetime
import uuid


def seed():
    print("STARTING SEED...")

    with Session(engine) as session:
        # clients
        client_a = Client(
            id=uuid.uuid4(),
            name="Client A",
            short_code="A"
        )
        client_b = Client(
            id=uuid.uuid4(),
            name="Client B",
            short_code="B"
        )
        session.add_all([client_a, client_b])

        # users
        agent = User(
            id=uuid.uuid4(),
            email="agent@test.com",
            name="Agent",
            role="agent"
        )
        director = User(
            id=uuid.uuid4(),
            email="director@test.com",
            name="Director",
            role="director"
        )
        session.add_all([agent, director])

        session.commit()  # commit so IDs are persisted

        # assignment
        assignment = UserClientAssignment(
            user_id=agent.id,
            client_id=client_a.id
        )
        session.add(assignment)

        # cases
        cases = []
        for i in range(5):
            case = DenialCase(
                id=uuid.uuid4(),
                client_id=client_a.id if i < 3 else client_b.id,
                case_number=f"C-{i}",
                payer_name="Aetna",
                denied_amount=100 + i,
                status="new",
                priority=3,
                created_at=datetime.utcnow()
            )
            cases.append(case)

        session.add_all(cases)

        session.commit()

        print("✅ Seed complete!")
        print("Agent ID:", agent.id)
        print("Director ID:", director.id)
        print("Client A ID:", client_a.id)
        print("Client B ID:", client_b.id)


if __name__ == "__main__":
    seed()
