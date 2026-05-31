from pathlib import Path
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.models import Base

DROSE_DIR = Path.home() / ".drose"
DROSE_DIR.mkdir(parents=True, exist_ok=True)
DROSE_DIR.chmod(0o700) # '0o' for octal, rwx for owner (he who executes this file) nothing for anyone else

DB_PATH = DROSE_DIR / "drose.db"
DB_PATH = DB_PATH.resolve()

DB_URL = os.getenv("DROSE_DB_URL", f"sqlite:///{DB_PATH}")

# SQLAlchemy's central object that knows how to talk to the database, Application -> Engine -> SQLite
# SQLite normally restricts a connection to the thread that created it, so we use check_same_thread = False
engine = create_engine(DB_URL, connect_args={"check_same_thread": False}) 

# SQLAlchemy looks at all models inheriting from Base
# and creates their tables, if missing, it does not update existing tables
# we use Alembic migrations for that
Base.metadata.create_all(bind=engine)

# factory that produces db sessions (a unit of work, tracks changes, sends SQL queries, manages transactions)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# when the file is imported, all what's above is executed

# whenever application code needs the database
def get_db_session():
    """Returns a new database session"""
    return SessionLocal()
