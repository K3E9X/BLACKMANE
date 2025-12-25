"""
Service layer for Flow business logic
"""

from fastapi import HTTPException, status
from repositories.flow_repository import FlowRepository
from models.flow import FlowCreate, FlowUpdate, Flow, FlowList


class FlowService:
    """Service for Flow business logic"""

    def __init__(self, repository: FlowRepository):
        self.repository = repository

    def _validate_flow(self, source_id: str, target_id: str) -> None:
        """Validate flow source and target are different"""
        if source_id == target_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Source and target components must be different"
            )

    def create_flow(self, flow_data: FlowCreate) -> Flow:
        """Create a new flow"""
        self._validate_flow(flow_data.source_component_id, flow_data.target_component_id)
        flow_orm = self.repository.create(flow_data)
        return Flow.model_validate(flow_orm)

    def get_flow(self, flow_id: str) -> Flow:
        """Get flow by ID"""
        flow_orm = self.repository.get_by_id(flow_id)
        if not flow_orm:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Flow {flow_id} not found"
            )
        return Flow.model_validate(flow_orm)

    def get_flows_by_architecture(self, architecture_id: str, skip: int = 0, limit: int = 100) -> FlowList:
        """Get all flows for an architecture"""
        flows_orm = self.repository.get_by_architecture(architecture_id, skip, limit)
        total = self.repository.count_by_architecture(architecture_id)
        return FlowList(
            flows=[Flow.model_validate(flow) for flow in flows_orm],
            total=total
        )

    def get_flows_by_component(self, component_id: str, skip: int = 0, limit: int = 100) -> FlowList:
        """Get all flows involving a component"""
        flows_orm = self.repository.get_by_component(component_id, skip, limit)
        return FlowList(
            flows=[Flow.model_validate(flow) for flow in flows_orm],
            total=len(flows_orm)
        )

    def get_all_flows(self, skip: int = 0, limit: int = 100) -> FlowList:
        """Get all flows"""
        flows_orm = self.repository.get_all(skip, limit)
        return FlowList(
            flows=[Flow.model_validate(flow) for flow in flows_orm],
            total=len(flows_orm)
        )

    def update_flow(self, flow_id: str, flow_data: FlowUpdate) -> Flow:
        """Update a flow"""
        flow_orm = self.repository.update(flow_id, flow_data)
        if not flow_orm:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Flow {flow_id} not found"
            )
        return Flow.model_validate(flow_orm)

    def delete_flow(self, flow_id: str) -> None:
        """Delete a flow"""
        if not self.repository.exists(flow_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Flow {flow_id} not found"
            )
        self.repository.delete(flow_id)
