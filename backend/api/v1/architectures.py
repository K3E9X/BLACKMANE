"""
API endpoints for Architecture CRUD operations
"""

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from database.connection import get_db
from repositories.architecture_repository import ArchitectureRepository
from services.architecture_service import ArchitectureService
from models.architecture import Architecture, ArchitectureCreate, ArchitectureUpdate

router = APIRouter()


def get_architecture_service(db: Session = Depends(get_db)) -> ArchitectureService:
    """Dependency injection for ArchitectureService"""
    repository = ArchitectureRepository(db)
    return ArchitectureService(repository)


@router.post(
    "/architectures",
    response_model=Architecture,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new architecture",
    description="Create a new architecture for a project. One architecture per project maximum."
)
def create_architecture(
    architecture: ArchitectureCreate,
    service: ArchitectureService = Depends(get_architecture_service)
):
    """Create a new architecture"""
    return service.create_architecture(architecture)


@router.get(
    "/architectures/{architecture_id}",
    response_model=Architecture,
    summary="Get architecture by ID",
    description="Retrieve a single architecture by its ID"
)
def get_architecture(
    architecture_id: str,
    service: ArchitectureService = Depends(get_architecture_service)
):
    """Get architecture by ID"""
    return service.get_architecture(architecture_id)


@router.get(
    "/projects/{project_id}/architecture",
    response_model=Architecture,
    summary="Get architecture for a project",
    description="Retrieve the architecture associated with a project"
)
def get_architecture_by_project(
    project_id: str,
    service: ArchitectureService = Depends(get_architecture_service)
):
    """Get architecture by project ID"""
    architecture = service.get_architecture_by_project(project_id)
    if not architecture:
        from fastapi import HTTPException
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No architecture found for project {project_id}"
        )
    return architecture


@router.put(
    "/architectures/{architecture_id}",
    response_model=Architecture,
    summary="Update architecture",
    description="Update an existing architecture"
)
def update_architecture(
    architecture_id: str,
    architecture: ArchitectureUpdate,
    service: ArchitectureService = Depends(get_architecture_service)
):
    """Update an architecture"""
    return service.update_architecture(architecture_id, architecture)


@router.delete(
    "/architectures/{architecture_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete architecture",
    description="Delete an architecture and all related data (zones, components, flows)"
)
def delete_architecture(
    architecture_id: str,
    service: ArchitectureService = Depends(get_architecture_service)
):
    """Delete an architecture"""
    service.delete_architecture(architecture_id)
