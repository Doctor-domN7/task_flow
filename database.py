from sqlalchemy import create_engine

from collections.abc import Generator

from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker




engine = create_engine("postgresql+psycopg://admin:admin@localhost:5433/todo_db")
SessionLocal = sessionmaker(bind=engine)
def get_db() -> Generator[Session, None, None]:
    with SessionLocal() as session:
        yield session

