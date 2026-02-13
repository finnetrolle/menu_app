"""
Database configuration and session management.
Uses SQLAlchemy 2.0 with support for both sync and async operations.
"""

from contextlib import contextmanager
from typing import Generator

from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session, relationship

from src.api.config import get_settings

# Get settings
settings = get_settings()

# Create base for models
Base = declarative_base()


class Ingredient(Base):
    """SQLAlchemy model for ingredients table."""
    __tablename__ = 'ingredients'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    protein_g = Column(Float, nullable=False)
    fat_g = Column(Float, nullable=False)
    carbohydrates_g = Column(Float, nullable=False)


class Dish(Base):
    """SQLAlchemy model for dishes table."""
    __tablename__ = 'dishes'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    ingredients = relationship('DishIngredient', back_populates='dish')


class DishIngredient(Base):
    """SQLAlchemy model for dish_ingredients junction table."""
    __tablename__ = 'dish_ingredients'
    
    dish_id = Column(Integer, ForeignKey('dishes.id'), primary_key=True)
    ingredient_id = Column(Integer, ForeignKey('ingredients.id'), primary_key=True)
    amount = Column(Float, nullable=False)
    
    dish = relationship('Dish', back_populates='ingredients')
    ingredient = relationship('Ingredient')


# Create engine with configuration from settings
engine = create_engine(
    settings.database_url,
    echo=settings.debug,  # Log SQL queries in debug mode
    pool_pre_ping=True,   # Enable connection health checks
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db() -> None:
    """Initialize database tables."""
    Base.metadata.create_all(engine)


@contextmanager
def get_session() -> Generator[Session, None, None]:
    """
    Context manager for database sessions.
    Ensures proper session cleanup even if exceptions occur.
    
    Usage:
        with get_session() as session:
            session.query(Dish).all()
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


def get_db() -> Generator[Session, None, None]:
    """
    FastAPI dependency for database sessions.
    
    Usage:
        @router.get("/dishes")
        async def get_dishes(db: Session = Depends(get_db)):
            return db.query(Dish).all()
    """
    with get_session() as session:
        yield session


# Initialize database on module import
init_db()
