"""
API endpoints for Zone CRUD operations
"""

from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session

from database.connection import get_db
from repositories.zone_repository import ZoneRepository
from services.zone_service import ZoneService
from models.zone import Zone, ZoneCreate, ZoneUpdate, ZoneList

router = APIRouter()


def get_zone_service(db: Session = Depends(get_db)) -> ZoneService:
    """Dependency injection for ZoneService"""
    repository = ZoneRepository(db)
    return ZoneService(repository)


@router.post(
    "/zones",
    response_model=Zone,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new zone",
    description="Create a new security zone within an architecture"
)
def create_zone(
    zone: ZoneCreate,
    service: ZoneService = Depends(get_zone_service)
):
    """Create a new zone"""
    return service.create_zone(zone)


@router.get(
    "/zones/{zone_id}",
    response_model=Zone,
    summary="Get zone by ID",
    description="Retrieve a single zone by its ID"
)
def get_zone(
    zone_id: str,
    service: ZoneService = Depends(get_zone_service)
):
    """Get zone by ID"""
    return service.get_zone(zone_id)


@router.get(
    "/architectures/{architecture_id}/zones",
    response_model=ZoneList,
    summary="Get zones for an architecture",
    description="Retrieve all zones for a specific architecture"
)
def get_zones_by_architecture(
    architecture_id: str,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    service: ZoneService = Depends(get_zone_service)
):
    """Get all zones for an architecture"""
    return service.get_zones_by_architecture(architecture_id, skip, limit)


@router.put(
    "/zones/{zone_id}",
    response_model=Zone,
    summary="Update zone",
    description="Update an existing zone"
)
def update_zone(
    zone_id: str,
    zone: ZoneUpdate,
    service: ZoneService = Depends(get_zone_service)
):
    """Update a zone"""
    return service.update_zone(zone_id, zone)


@router.delete(
    "/zones/{zone_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete zone",
    description="Delete a zone and all components within it"
)
def delete_zone(
    zone_id: str,
    service: ZoneService = Depends(get_zone_service)
):
    """Delete a zone"""
    service.delete_zone(zone_id)
