"""
API endpoints for Component CRUD operations
"""

from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session

from database.connection import get_db
from repositories.component_repository import ComponentRepository
from services.component_service import ComponentService
from models.component import Component, ComponentCreate, ComponentUpdate, ComponentList

router = APIRouter()


def get_component_service(db: Session = Depends(get_db)) -> ComponentService:
    """Dependency injection for ComponentService"""
    repository = ComponentRepository(db)
    return ComponentService(repository)


@router.post(
    "/components",
    response_model=Component,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new component",
    description="Create a new component within a zone"
)
def create_component(
    component: ComponentCreate,
    service: ComponentService = Depends(get_component_service)
):
    """Create a new component"""
    return service.create_component(component)


@router.get(
    "/components/{component_id}",
    response_model=Component,
    summary="Get component by ID",
    description="Retrieve a single component by its ID"
)
def get_component(
    component_id: str,
    service: ComponentService = Depends(get_component_service)
):
    """Get component by ID"""
    return service.get_component(component_id)


@router.get(
    "/architectures/{architecture_id}/components",
    response_model=ComponentList,
    summary="Get components for an architecture",
    description="Retrieve all components for a specific architecture"
)
def get_components_by_architecture(
    architecture_id: str,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    service: ComponentService = Depends(get_component_service)
):
    """Get all components for an architecture"""
    return service.get_components_by_architecture(architecture_id, skip, limit)


@router.get(
    "/zones/{zone_id}/components",
    response_model=ComponentList,
    summary="Get components for a zone",
    description="Retrieve all components within a specific zone"
)
def get_components_by_zone(
    zone_id: str,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    service: ComponentService = Depends(get_component_service)
):
    """Get all components in a zone"""
    return service.get_components_by_zone(zone_id, skip, limit)


@router.put(
    "/components/{component_id}",
    response_model=Component,
    summary="Update component",
    description="Update an existing component"
)
def update_component(
    component_id: str,
    component: ComponentUpdate,
    service: ComponentService = Depends(get_component_service)
):
    """Update a component"""
    return service.update_component(component_id, component)


@router.delete(
    "/components/{component_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete component",
    description="Delete a component and all flows involving it"
)
def delete_component(
    component_id: str,
    service: ComponentService = Depends(get_component_service)
):
    """Delete a component"""
    service.delete_component(component_id)
