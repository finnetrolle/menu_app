"""
Base repository with common CRUD operations.
"""

from abc import ABC, abstractmethod
from typing import Generic, TypeVar, List, Optional, Type
from sqlalchemy.orm import Session

from src.database import Base

# Generic type variables
ModelType = TypeVar("ModelType", bound=Base)


class BaseRepository(ABC, Generic[ModelType]):
    """
    Abstract base repository providing common database operations.
    
    Subclasses should implement:
    - model: The SQLAlchemy model class
    - Any custom query methods
    """
    
    def __init__(self, db: Session):
        """
        Initialize repository with database session.
        
        Args:
            db: SQLAlchemy session for database operations
        """
        self.db = db
    
    @property
    @abstractmethod
    def model(self) -> Type[ModelType]:
        """Return the SQLAlchemy model class."""
        pass
    
    def get_by_id(self, id: int) -> Optional[ModelType]:
        """
        Get a single record by ID.
        
        Args:
            id: Primary key value
            
        Returns:
            Model instance or None if not found
        """
        return self.db.query(self.model).filter(self.model.id == id).first()
    
    def get_all(self, skip: int = 0, limit: int = 100) -> List[ModelType]:
        """
        Get all records with optional pagination.
        
        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List of model instances
        """
        return self.db.query(self.model).offset(skip).limit(limit).all()
    
    def create(self, obj: ModelType) -> ModelType:
        """
        Create a new record.
        
        Args:
            obj: Model instance to create
            
        Returns:
            Created model instance with ID populated
        """
        self.db.add(obj)
        self.db.flush()  # Flush to get the ID
        return obj
    
    def update(self, obj: ModelType) -> ModelType:
        """
        Update an existing record.
        
        Args:
            obj: Model instance with updated values
            
        Returns:
            Updated model instance
        """
        self.db.merge(obj)
        self.db.flush()
        return obj
    
    def delete(self, id: int) -> bool:
        """
        Delete a record by ID.
        
        Args:
            id: Primary key value
            
        Returns:
            True if deleted, False if not found
        """
        obj = self.get_by_id(id)
        if obj:
            self.db.delete(obj)
            self.db.flush()
            return True
        return False
    
    def count(self) -> int:
        """
        Get total count of records.
        
        Returns:
            Number of records
        """
        return self.db.query(self.model).count()
    
    def exists(self, id: int) -> bool:
        """
        Check if a record exists.
        
        Args:
            id: Primary key value
            
        Returns:
            True if exists, False otherwise
        """
        return self.get_by_id(id) is not None
