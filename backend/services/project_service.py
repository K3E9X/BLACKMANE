"""
Project Service - Business logic for projects

Handles all business logic for project management
"""

from typing import Optional, List
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from models.project import Project, ProjectCreate, ProjectUpdate, ProjectList
from repositories.project_repository import ProjectRepository


class ProjectService:
    """Service for project business logic"""

    def __init__(self, db: Session):
        self.db = db
        self.repository = ProjectRepository(db)

    def create_project(self, project_data: ProjectCreate) -> Project:
        """
        Create a new project

        Args:
            project_data: Project creation data

        Returns:
            Created project

        Raises:
            HTTPException: If validation fails
        """
        # Business validations
        self._validate_project_name(project_data.name)

        # Create project
        project_orm = self.repository.create(project_data)

        # Convert to Pydantic model
        return Project.model_validate(project_orm)

    def get_project(self, project_id: str) -> Project:
        """
        Get a project by ID

        Args:
            project_id: Project UUID

        Returns:
            Project

        Raises:
            HTTPException: If project not found
        """
        project_orm = self.repository.get_by_id(project_id)
        if not project_orm:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Project with ID {project_id} not found"
            )

        return Project.model_validate(project_orm)

    def list_projects(self, skip: int = 0, limit: int = 100) -> ProjectList:
        """
        List all projects with pagination

        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of projects with total count
        """
        projects_orm = self.repository.get_all(skip=skip, limit=limit)
        total = self.repository.count()

        projects = [Project.model_validate(p) for p in projects_orm]

        return ProjectList(projects=projects, total=total)

    def update_project(self, project_id: str, project_data: ProjectUpdate) -> Project:
        """
        Update a project

        Args:
            project_id: Project UUID
            project_data: Update data

        Returns:
            Updated project

        Raises:
            HTTPException: If project not found or validation fails
        """
        # Check if project exists
        if not self.repository.exists(project_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Project with ID {project_id} not found"
            )

        # Validate name if provided
        if project_data.name:
            self._validate_project_name(project_data.name)

        # Update project
        project_orm = self.repository.update(project_id, project_data)

        return Project.model_validate(project_orm)

    def delete_project(self, project_id: str) -> None:
        """
        Delete a project

        Args:
            project_id: Project UUID

        Raises:
            HTTPException: If project not found
        """
        deleted = self.repository.delete(project_id)
        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Project with ID {project_id} not found"
            )

    def _validate_project_name(self, name: str) -> None:
        """
        Validate project name

        Args:
            name: Project name

        Raises:
            HTTPException: If validation fails
        """
        if not name or not name.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Project name cannot be empty"
            )

        if len(name) > 200:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Project name cannot exceed 200 characters"
            )
