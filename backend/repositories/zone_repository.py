"""
Repository for Zone entity
"""

import uuid
from typing import Optional
from sqlalchemy.orm import Session
from models.orm import Zone
from models.zone import ZoneCreate, ZoneUpdate


class ZoneRepository:
    """Repository for Zone CRUD operations"""

    def __init__(self, db: Session):
        self.db = db

    def create(self, zone_data: ZoneCreate) -> Zone:
        """Create a new zone"""
        zone = Zone(
            id=str(uuid.uuid4()),
            architecture_id=zone_data.architecture_id,
            name=zone_data.name,
            trust_level=zone_data.trust_level,
            description=zone_data.description
        )
        self.db.add(zone)
        self.db.commit()
        self.db.refresh(zone)
        return zone

    def get_by_id(self, zone_id: str) -> Optional[Zone]:
        """Get zone by ID"""
        return self.db.query(Zone).filter(Zone.id == zone_id).first()

    def get_by_architecture(self, architecture_id: str, skip: int = 0, limit: int = 100) -> list[Zone]:
        """Get all zones for an architecture"""
        return self.db.query(Zone).filter(
            Zone.architecture_id == architecture_id
        ).offset(skip).limit(limit).all()

    def get_all(self, skip: int = 0, limit: int = 100) -> list[Zone]:
        """Get all zones with pagination"""
        return self.db.query(Zone).offset(skip).limit(limit).all()

    def update(self, zone_id: str, zone_data: ZoneUpdate) -> Optional[Zone]:
        """Update a zone"""
        zone = self.get_by_id(zone_id)
        if not zone:
            return None

        update_data = zone_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(zone, field, value)

        self.db.commit()
        self.db.refresh(zone)
        return zone

    def delete(self, zone_id: str) -> bool:
        """Delete a zone"""
        zone = self.get_by_id(zone_id)
        if not zone:
            return False

        self.db.delete(zone)
        self.db.commit()
        return True

    def exists(self, zone_id: str) -> bool:
        """Check if zone exists"""
        return self.db.query(Zone).filter(Zone.id == zone_id).count() > 0

    def count_by_architecture(self, architecture_id: str) -> int:
        """Count zones for an architecture"""
        return self.db.query(Zone).filter(Zone.architecture_id == architecture_id).count()
