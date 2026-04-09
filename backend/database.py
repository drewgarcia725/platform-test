from sqlmodel import SQLModel, create_engine, Session

engine = create_engine("sqlite:///database.db", echo=False)

def get_session():
    with Session(engine) as session:
        yield session

def init_db():
    SQLModel.metadata.create_all(engine)
