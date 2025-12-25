"""
Service layer for Architecture business logic
"""

from typing import Optional
from fastapi import HTTPException, status
from repositories.architecture_repository import ArchitectureRepository
from models.architecture import ArchitectureCreate, ArchitectureUpdate, Architecture


class ArchitectureService:
    """Service for Architecture business logic"""

    def __init__(self, repository: ArchitectureRepository):
        self.repository = repository

    def create_architecture(self, architecture_data: ArchitectureCreate) -> Architecture:
        """Create a new architecture"""
        # Check if architecture already exists for this project
        existing = self.repository.get_by_project_id(architecture_data.project_id)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Architecture already exists for project {architecture_data.project_id}"
            )

        architecture_orm = self.repository.create(architecture_data)
        return Architecture.model_validate(architecture_orm)

    def get_architecture(self, architecture_id: str) -> Architecture:
        """Get architecture by ID"""
        architecture_orm = self.repository.get_by_id(architecture_id)
        if not architecture_orm:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Architecture {architecture_id} not found"
            )
        return Architecture.model_validate(architecture_orm)

    def get_architecture_by_project(self, project_id: str) -> Optional[Architecture]:
        """Get architecture by project ID"""
        architecture_orm = self.repository.get_by_project_id(project_id)
        if not architecture_orm:
            return None
        return Architecture.model_validate(architecture_orm)

    def get_all_architectures(self, skip: int = 0, limit: int = 100) -> list[Architecture]:
        """Get all architectures"""
        architectures_orm = self.repository.get_all(skip, limit)
        return [Architecture.model_validate(arch) for arch in architectures_orm]

    def update_architecture(self, architecture_id: str, architecture_data: ArchitectureUpdate) -> Architecture:
        """Update an architecture"""
        architecture_orm = self.repository.update(architecture_id, architecture_data)
        if not architecture_orm:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Architecture {architecture_id} not found"
            )
        return Architecture.model_validate(architecture_orm)

    def delete_architecture(self, architecture_id: str) -> None:
        """Delete an architecture"""
        if not self.repository.exists(architecture_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Architecture {architecture_id} not found"
            )
        self.repository.delete(architecture_id)

    def get_total_count(self) -> int:
        """Get total count of architectures"""
        return self.repository.count()
