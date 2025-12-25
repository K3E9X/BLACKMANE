"""
Repository for Flow entity
"""

import uuid
from typing import Optional
from sqlalchemy.orm import Session
from models.orm import Flow
from models.flow import FlowCreate, FlowUpdate


class FlowRepository:
    """Repository for Flow CRUD operations"""

    def __init__(self, db: Session):
        self.db = db

    def create(self, flow_data: FlowCreate) -> Flow:
        """Create a new flow"""
        flow = Flow(
            id=str(uuid.uuid4()),
            architecture_id=flow_data.architecture_id,
            source_component_id=flow_data.source_component_id,
            target_component_id=flow_data.target_component_id,
            protocol=flow_data.protocol,
            port=flow_data.port,
            is_authenticated=flow_data.is_authenticated,
            is_encrypted=flow_data.is_encrypted,
            description=flow_data.description
        )
        self.db.add(flow)
        self.db.commit()
        self.db.refresh(flow)
        return flow

    def get_by_id(self, flow_id: str) -> Optional[Flow]:
        """Get flow by ID"""
        return self.db.query(Flow).filter(Flow.id == flow_id).first()

    def get_by_architecture(self, architecture_id: str, skip: int = 0, limit: int = 100) -> list[Flow]:
        """Get all flows for an architecture"""
        return self.db.query(Flow).filter(
            Flow.architecture_id == architecture_id
        ).offset(skip).limit(limit).all()

    def get_by_component(self, component_id: str, skip: int = 0, limit: int = 100) -> list[Flow]:
        """Get all flows involving a component (as source or target)"""
        return self.db.query(Flow).filter(
            (Flow.source_component_id == component_id) | (Flow.target_component_id == component_id)
        ).offset(skip).limit(limit).all()

    def get_all(self, skip: int = 0, limit: int = 100) -> list[Flow]:
        """Get all flows with pagination"""
        return self.db.query(Flow).offset(skip).limit(limit).all()

    def update(self, flow_id: str, flow_data: FlowUpdate) -> Optional[Flow]:
        """Update a flow"""
        flow = self.get_by_id(flow_id)
        if not flow:
            return None

        update_data = flow_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(flow, field, value)

        self.db.commit()
        self.db.refresh(flow)
        return flow

    def delete(self, flow_id: str) -> bool:
        """Delete a flow"""
        flow = self.get_by_id(flow_id)
        if not flow:
            return False

        self.db.delete(flow)
        self.db.commit()
        return True

    def exists(self, flow_id: str) -> bool:
        """Check if flow exists"""
        return self.db.query(Flow).filter(Flow.id == flow_id).count() > 0

    def count_by_architecture(self, architecture_id: str) -> int:
        """Count flows for an architecture"""
        return self.db.query(Flow).filter(Flow.architecture_id == architecture_id).count()
