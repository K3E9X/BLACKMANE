"""
Service layer for Zone business logic
"""

from fastapi import HTTPException, status
from repositories.zone_repository import ZoneRepository
from models.zone import ZoneCreate, ZoneUpdate, Zone, ZoneList


class ZoneService:
    """Service for Zone business logic"""

    def __init__(self, repository: ZoneRepository):
        self.repository = repository

    def _validate_zone_name(self, name: str, architecture_id: str, exclude_id: str = None) -> None:
        """Validate zone name is not empty and is unique within architecture"""
        if not name or not name.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Zone name cannot be empty"
            )

    def create_zone(self, zone_data: ZoneCreate) -> Zone:
        """Create a new zone"""
        self._validate_zone_name(zone_data.name, zone_data.architecture_id)
        zone_orm = self.repository.create(zone_data)
        return Zone.model_validate(zone_orm)

    def get_zone(self, zone_id: str) -> Zone:
        """Get zone by ID"""
        zone_orm = self.repository.get_by_id(zone_id)
        if not zone_orm:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Zone {zone_id} not found"
            )
        return Zone.model_validate(zone_orm)

    def get_zones_by_architecture(self, architecture_id: str, skip: int = 0, limit: int = 100) -> ZoneList:
        """Get all zones for an architecture"""
        zones_orm = self.repository.get_by_architecture(architecture_id, skip, limit)
        total = self.repository.count_by_architecture(architecture_id)
        return ZoneList(
            zones=[Zone.model_validate(zone) for zone in zones_orm],
            total=total
        )

    def get_all_zones(self, skip: int = 0, limit: int = 100) -> ZoneList:
        """Get all zones"""
        zones_orm = self.repository.get_all(skip, limit)
        return ZoneList(
            zones=[Zone.model_validate(zone) for zone in zones_orm],
            total=len(zones_orm)
        )

    def update_zone(self, zone_id: str, zone_data: ZoneUpdate) -> Zone:
        """Update a zone"""
        if zone_data.name:
            zone = self.repository.get_by_id(zone_id)
            if zone:
                self._validate_zone_name(zone_data.name, zone.architecture_id, zone_id)

        zone_orm = self.repository.update(zone_id, zone_data)
        if not zone_orm:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Zone {zone_id} not found"
            )
        return Zone.model_validate(zone_orm)

    def delete_zone(self, zone_id: str) -> None:
        """Delete a zone"""
        if not self.repository.exists(zone_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Zone {zone_id} not found"
            )
        self.repository.delete(zone_id)
