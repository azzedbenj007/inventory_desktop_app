"""
SQLAlchemy engine, session factory, and Base declaration.
All models import Base and Session from here.
"""
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Resolve the SQLite file path relative to the project root
_DB_DIR = Path(__file__).resolve().parents[2] / "data"
_DB_DIR.mkdir(parents=True, exist_ok=True)
_DB_PATH = _DB_DIR / "inventory.db"

DATABASE_URL = f"sqlite:///{_DB_PATH}"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
    echo=False,
)

SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
)

Base = declarative_base()


def init_db() -> None:
    """Create all tables if they do not already exist."""
    from src.models import product  # noqa: F401 — ensures models are registered
    Base.metadata.create_all(bind=engine)


def get_session():
    """
    Yield a SQLAlchemy session and guarantee it is closed after use.

    Usage:
        with get_session() as session:
            ...
    """
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
