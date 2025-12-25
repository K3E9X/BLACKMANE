"""
Repository for Component entity
"""

import uuid
from typing import Optional
from sqlalchemy.orm import Session
from models.orm import Component
from models.component import ComponentCreate, ComponentUpdate


class ComponentRepository:
    """Repository for Component CRUD operations"""

    def __init__(self, db: Session):
        self.db = db

    def create(self, component_data: ComponentCreate) -> Component:
        """Create a new component"""
        component = Component(
            id=str(uuid.uuid4()),
            architecture_id=component_data.architecture_id,
            zone_id=component_data.zone_id,
            name=component_data.name,
            component_type=component_data.component_type,
            has_admin_interface=component_data.has_admin_interface,
            requires_mfa=component_data.requires_mfa,
            has_logging=component_data.has_logging,
            encryption_at_rest=component_data.encryption_at_rest,
            encryption_in_transit=component_data.encryption_in_transit,
            description=component_data.description
        )
        self.db.add(component)
        self.db.commit()
        self.db.refresh(component)
        return component

    def get_by_id(self, component_id: str) -> Optional[Component]:
        """Get component by ID"""
        return self.db.query(Component).filter(Component.id == component_id).first()

    def get_by_architecture(self, architecture_id: str, skip: int = 0, limit: int = 100) -> list[Component]:
        """Get all components for an architecture"""
        return self.db.query(Component).filter(
            Component.architecture_id == architecture_id
        ).offset(skip).limit(limit).all()

    def get_by_zone(self, zone_id: str, skip: int = 0, limit: int = 100) -> list[Component]:
        """Get all components in a zone"""
        return self.db.query(Component).filter(
            Component.zone_id == zone_id
        ).offset(skip).limit(limit).all()

    def get_all(self, skip: int = 0, limit: int = 100) -> list[Component]:
        """Get all components with pagination"""
        return self.db.query(Component).offset(skip).limit(limit).all()

    def update(self, component_id: str, component_data: ComponentUpdate) -> Optional[Component]:
        """Update a component"""
        component = self.get_by_id(component_id)
        if not component:
            return None

        update_data = component_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(component, field, value)

        self.db.commit()
        self.db.refresh(component)
        return component

    def delete(self, component_id: str) -> bool:
        """Delete a component"""
        component = self.get_by_id(component_id)
        if not component:
            return False

        self.db.delete(component)
        self.db.commit()
        return True

    def exists(self, component_id: str) -> bool:
        """Check if component exists"""
        return self.db.query(Component).filter(Component.id == component_id).count() > 0

    def count_by_architecture(self, architecture_id: str) -> int:
        """Count components for an architecture"""
        return self.db.query(Component).filter(Component.architecture_id == architecture_id).count()

    def count_by_zone(self, zone_id: str) -> int:
        """Count components in a zone"""
        return self.db.query(Component).filter(Component.zone_id == zone_id).count()
