"""
Projects API Routes

REST API endpoints for project management
"""

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from database.connection import get_db
from models.project import Project, ProjectCreate, ProjectUpdate, ProjectList
from services.project_service import ProjectService

router = APIRouter()


def get_project_service(db: Session = Depends(get_db)) -> ProjectService:
    """Dependency to get ProjectService instance"""
    return ProjectService(db)


@router.post(
    "/projects",
    response_model=Project,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new project",
    description="Create a new architecture analysis project",
    tags=["Projects"]
)
def create_project(
    project: ProjectCreate,
    service: ProjectService = Depends(get_project_service)
) -> Project:
    """
    Create a new project.

    - **name**: Project name (required)
    - **project_type**: Type of infrastructure (cloud, on-premise, hybrid)
    - **business_context**: Business context and objectives (optional)
    - **criticality_level**: Criticality level (low, medium, high, critical)
    """
    return service.create_project(project)


@router.get(
    "/projects",
    response_model=ProjectList,
    summary="List all projects",
    description="Get a list of all architecture analysis projects",
    tags=["Projects"]
)
def list_projects(
    skip: int = 0,
    limit: int = 100,
    service: ProjectService = Depends(get_project_service)
) -> ProjectList:
    """
    List all projects with pagination.

    - **skip**: Number of records to skip (default: 0)
    - **limit**: Maximum number of records to return (default: 100, max: 100)
    """
    if limit > 100:
        limit = 100
    return service.list_projects(skip=skip, limit=limit)


@router.get(
    "/projects/{project_id}",
    response_model=Project,
    summary="Get a project",
    description="Get a specific project by ID",
    tags=["Projects"]
)
def get_project(
    project_id: str,
    service: ProjectService = Depends(get_project_service)
) -> Project:
    """
    Get a project by ID.

    - **project_id**: Project UUID
    """
    return service.get_project(project_id)


@router.put(
    "/projects/{project_id}",
    response_model=Project,
    summary="Update a project",
    description="Update a project's information",
    tags=["Projects"]
)
def update_project(
    project_id: str,
    project: ProjectUpdate,
    service: ProjectService = Depends(get_project_service)
) -> Project:
    """
    Update a project.

    - **project_id**: Project UUID
    - **name**: Updated project name (optional)
    - **business_context**: Updated business context (optional)
    - **criticality_level**: Updated criticality level (optional)
    """
    return service.update_project(project_id, project)


@router.delete(
    "/projects/{project_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a project",
    description="Delete a project and all associated data",
    tags=["Projects"]
)
def delete_project(
    project_id: str,
    service: ProjectService = Depends(get_project_service)
) -> None:
    """
    Delete a project.

    This will also delete:
    - Architecture
    - All components, zones, and flows
    - All analyses and findings
    - All recommendations

    - **project_id**: Project UUID
    """
    service.delete_project(project_id)
