"""
API endpoints for Flow CRUD operations
"""

from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session

from database.connection import get_db
from repositories.flow_repository import FlowRepository
from services.flow_service import FlowService
from models.flow import Flow, FlowCreate, FlowUpdate, FlowList

router = APIRouter()


def get_flow_service(db: Session = Depends(get_db)) -> FlowService:
    """Dependency injection for FlowService"""
    repository = FlowRepository(db)
    return FlowService(repository)


@router.post(
    "/flows",
    response_model=Flow,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new flow",
    description="Create a new data flow between components"
)
def create_flow(
    flow: FlowCreate,
    service: FlowService = Depends(get_flow_service)
):
    """Create a new flow"""
    return service.create_flow(flow)


@router.get(
    "/flows/{flow_id}",
    response_model=Flow,
    summary="Get flow by ID",
    description="Retrieve a single flow by its ID"
)
def get_flow(
    flow_id: str,
    service: FlowService = Depends(get_flow_service)
):
    """Get flow by ID"""
    return service.get_flow(flow_id)


@router.get(
    "/architectures/{architecture_id}/flows",
    response_model=FlowList,
    summary="Get flows for an architecture",
    description="Retrieve all data flows for a specific architecture"
)
def get_flows_by_architecture(
    architecture_id: str,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    service: FlowService = Depends(get_flow_service)
):
    """Get all flows for an architecture"""
    return service.get_flows_by_architecture(architecture_id, skip, limit)


@router.get(
    "/components/{component_id}/flows",
    response_model=FlowList,
    summary="Get flows for a component",
    description="Retrieve all flows involving a specific component (as source or target)"
)
def get_flows_by_component(
    component_id: str,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    service: FlowService = Depends(get_flow_service)
):
    """Get all flows involving a component"""
    return service.get_flows_by_component(component_id, skip, limit)


@router.put(
    "/flows/{flow_id}",
    response_model=Flow,
    summary="Update flow",
    description="Update an existing flow"
)
def update_flow(
    flow_id: str,
    flow: FlowUpdate,
    service: FlowService = Depends(get_flow_service)
):
    """Update a flow"""
    return service.update_flow(flow_id, flow)


@router.delete(
    "/flows/{flow_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete flow",
    description="Delete a data flow"
)
def delete_flow(
    flow_id: str,
    service: FlowService = Depends(get_flow_service)
):
    """Delete a flow"""
    service.delete_flow(flow_id)
