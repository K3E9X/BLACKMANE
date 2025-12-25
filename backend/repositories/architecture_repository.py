"""
Repository for Architecture entity
"""

import uuid
from typing import Optional
from sqlalchemy.orm import Session
from models.orm import Architecture
from models.architecture import ArchitectureCreate, ArchitectureUpdate


class ArchitectureRepository:
    """Repository for Architecture CRUD operations"""

    def __init__(self, db: Session):
        self.db = db

    def create(self, architecture_data: ArchitectureCreate) -> Architecture:
        """Create a new architecture"""
        architecture = Architecture(
            id=str(uuid.uuid4()),
            project_id=architecture_data.project_id,
            description=architecture_data.description
        )
        self.db.add(architecture)
        self.db.commit()
        self.db.refresh(architecture)
        return architecture

    def get_by_id(self, architecture_id: str) -> Optional[Architecture]:
        """Get architecture by ID"""
        return self.db.query(Architecture).filter(Architecture.id == architecture_id).first()

    def get_by_project_id(self, project_id: str) -> Optional[Architecture]:
        """Get architecture by project ID"""
        return self.db.query(Architecture).filter(Architecture.project_id == project_id).first()

    def get_all(self, skip: int = 0, limit: int = 100) -> list[Architecture]:
        """Get all architectures with pagination"""
        return self.db.query(Architecture).offset(skip).limit(limit).all()

    def update(self, architecture_id: str, architecture_data: ArchitectureUpdate) -> Optional[Architecture]:
        """Update an architecture"""
        architecture = self.get_by_id(architecture_id)
        if not architecture:
            return None

        update_data = architecture_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(architecture, field, value)

        self.db.commit()
        self.db.refresh(architecture)
        return architecture

    def delete(self, architecture_id: str) -> bool:
        """Delete an architecture"""
        architecture = self.get_by_id(architecture_id)
        if not architecture:
            return False

        self.db.delete(architecture)
        self.db.commit()
        return True

    def exists(self, architecture_id: str) -> bool:
        """Check if architecture exists"""
        return self.db.query(Architecture).filter(Architecture.id == architecture_id).count() > 0

    def count(self) -> int:
        """Count total architectures"""
        return self.db.query(Architecture).count()
