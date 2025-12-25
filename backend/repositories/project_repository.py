"""
Project Repository - Data access layer for projects

Handles all database operations for projects
"""

from typing import Optional, List
from sqlalchemy.orm import Session
from models.orm import Project as ProjectORM
from models.project import ProjectCreate, ProjectUpdate
import uuid


class ProjectRepository:
    """Repository for project database operations"""

    def __init__(self, db: Session):
        self.db = db

    def create(self, project_data: ProjectCreate) -> ProjectORM:
        """
        Create a new project in database

        Args:
            project_data: Project creation data

        Returns:
            Created project ORM model
        """
        project = ProjectORM(
            id=str(uuid.uuid4()),
            name=project_data.name,
            project_type=project_data.project_type,
            business_context=project_data.business_context,
            criticality_level=project_data.criticality_level
        )
        self.db.add(project)
        self.db.commit()
        self.db.refresh(project)
        return project

    def get_by_id(self, project_id: str) -> Optional[ProjectORM]:
        """
        Get a project by ID

        Args:
            project_id: Project UUID

        Returns:
            Project ORM model or None if not found
        """
        return self.db.query(ProjectORM).filter(ProjectORM.id == project_id).first()

    def get_all(self, skip: int = 0, limit: int = 100) -> List[ProjectORM]:
        """
        Get all projects with pagination

        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of project ORM models
        """
        return self.db.query(ProjectORM).offset(skip).limit(limit).all()

    def count(self) -> int:
        """
        Count total number of projects

        Returns:
            Total count of projects
        """
        return self.db.query(ProjectORM).count()

    def update(self, project_id: str, project_data: ProjectUpdate) -> Optional[ProjectORM]:
        """
        Update a project

        Args:
            project_id: Project UUID
            project_data: Update data (only non-None fields will be updated)

        Returns:
            Updated project ORM model or None if not found
        """
        project = self.get_by_id(project_id)
        if not project:
            return None

        # Update only provided fields
        update_data = project_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(project, field, value)

        self.db.commit()
        self.db.refresh(project)
        return project

    def delete(self, project_id: str) -> bool:
        """
        Delete a project

        Args:
            project_id: Project UUID

        Returns:
            True if deleted, False if not found
        """
        project = self.get_by_id(project_id)
        if not project:
            return False

        self.db.delete(project)
        self.db.commit()
        return True

    def exists(self, project_id: str) -> bool:
        """
        Check if a project exists

        Args:
            project_id: Project UUID

        Returns:
            True if exists, False otherwise
        """
        return self.db.query(ProjectORM).filter(ProjectORM.id == project_id).count() > 0
