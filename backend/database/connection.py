"""
Database connection and session management
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.pool import StaticPool

from config import get_settings

settings = get_settings()

# Create SQLite engine
# Using StaticPool for SQLite to handle concurrent access
engine = create_engine(
    settings.database_url,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for ORM models
Base = declarative_base()


def get_db():
    """
    Dependency for FastAPI to get database session

    Usage in routes:
        @app.get("/items")
        def get_items(db: Session = Depends(get_db)):
            ...
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Initialize database schema"""
    # Import all ORM models here to ensure they're registered
    # from models.orm import Project, Architecture, Zone, Component, Flow, ...

    # Create all tables
    Base.metadata.create_all(bind=engine)
    print("Database initialized successfully")


def drop_db():
    """Drop all tables (for testing only)"""
    Base.metadata.drop_all(bind=engine)
    print("Database dropped")
