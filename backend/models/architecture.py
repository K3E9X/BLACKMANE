"""
Pydantic models for Architecture entity
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class ArchitectureCreate(BaseModel):
    """Schema for creating an architecture"""
    project_id: str = Field(..., min_length=36, max_length=36, description="Project ID")
    description: Optional[str] = Field(None, description="Architecture description")

    model_config = {
        "json_schema_extra": {
            "examples": [{
                "project_id": "123e4567-e89b-12d3-a456-426614174000",
                "description": "Kubernetes-based microservices architecture"
            }]
        }
    }


class ArchitectureUpdate(BaseModel):
    """Schema for updating an architecture"""
    description: Optional[str] = Field(None, description="Architecture description")

    model_config = {
        "json_schema_extra": {
            "examples": [{
                "description": "Updated architecture description"
            }]
        }
    }


class Architecture(BaseModel):
    """Schema for architecture response"""
    id: str
    project_id: str
    description: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "examples": [{
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "project_id": "123e4567-e89b-12d3-a456-426614174001",
                "description": "Kubernetes-based architecture",
                "created_at": "2025-12-25T10:00:00",
                "updated_at": "2025-12-25T10:00:00"
            }]
        }
    }
