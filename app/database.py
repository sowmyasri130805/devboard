from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# This creates a local SQLite database file called devboard.db
DATABASE_URL = "sqlite:///./devboard.db"

# Engine = actual connection to the database
engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)

# SessionLocal = used to talk to the database (run queries)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base = all our models will inherit from this
Base = declarative_base()

# This function gives us a database session for each request
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()