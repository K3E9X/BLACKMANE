"""
Service layer for Component business logic
"""

from fastapi import HTTPException, status
from repositories.component_repository import ComponentRepository
from models.component import ComponentCreate, ComponentUpdate, Component, ComponentList


class ComponentService:
    """Service for Component business logic"""

    def __init__(self, repository: ComponentRepository):
        self.repository = repository

    def _validate_component_name(self, name: str) -> None:
        """Validate component name is not empty"""
        if not name or not name.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Component name cannot be empty"
            )

    def create_component(self, component_data: ComponentCreate) -> Component:
        """Create a new component"""
        self._validate_component_name(component_data.name)
        component_orm = self.repository.create(component_data)
        return Component.model_validate(component_orm)

    def get_component(self, component_id: str) -> Component:
        """Get component by ID"""
        component_orm = self.repository.get_by_id(component_id)
        if not component_orm:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Component {component_id} not found"
            )
        return Component.model_validate(component_orm)

    def get_components_by_architecture(self, architecture_id: str, skip: int = 0, limit: int = 100) -> ComponentList:
        """Get all components for an architecture"""
        components_orm = self.repository.get_by_architecture(architecture_id, skip, limit)
        total = self.repository.count_by_architecture(architecture_id)
        return ComponentList(
            components=[Component.model_validate(comp) for comp in components_orm],
            total=total
        )

    def get_components_by_zone(self, zone_id: str, skip: int = 0, limit: int = 100) -> ComponentList:
        """Get all components in a zone"""
        components_orm = self.repository.get_by_zone(zone_id, skip, limit)
        total = self.repository.count_by_zone(zone_id)
        return ComponentList(
            components=[Component.model_validate(comp) for comp in components_orm],
            total=total
        )

    def get_all_components(self, skip: int = 0, limit: int = 100) -> ComponentList:
        """Get all components"""
        components_orm = self.repository.get_all(skip, limit)
        return ComponentList(
            components=[Component.model_validate(comp) for comp in components_orm],
            total=len(components_orm)
        )

    def update_component(self, component_id: str, component_data: ComponentUpdate) -> Component:
        """Update a component"""
        if component_data.name:
            self._validate_component_name(component_data.name)

        component_orm = self.repository.update(component_id, component_data)
        if not component_orm:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Component {component_id} not found"
            )
        return Component.model_validate(component_orm)

    def delete_component(self, component_id: str) -> None:
        """Delete a component"""
        if not self.repository.exists(component_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Component {component_id} not found"
            )
        self.repository.delete(component_id)
