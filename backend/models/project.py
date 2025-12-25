"""
Pydantic models for Project API

Request/Response schemas for project endpoints
"""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum


class ProjectType(str, Enum):
    """Project type enumeration"""
    CLOUD = "cloud"
    ON_PREMISE = "on-premise"
    HYBRID = "hybrid"


class CriticalityLevel(str, Enum):
    """Criticality level enumeration"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class ProjectCreate(BaseModel):
    """Schema for creating a new project"""
    name: str = Field(..., min_length=1, max_length=200, description="Project name")
    project_type: ProjectType = Field(..., description="Type of infrastructure")
    business_context: Optional[str] = Field(None, description="Business context and objectives")
    criticality_level: CriticalityLevel = Field(..., description="Criticality level")

    model_config = {
        "json_schema_extra": {
            "example": {
                "name": "Production API Platform",
                "project_type": "cloud",
                "business_context": "SaaS API serving 100k users",
                "criticality_level": "high"
            }
        }
    }


class ProjectUpdate(BaseModel):
    """Schema for updating a project"""
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    business_context: Optional[str] = None
    criticality_level: Optional[CriticalityLevel] = None

    model_config = {
        "json_schema_extra": {
            "example": {
                "name": "Updated Project Name",
                "criticality_level": "critical"
            }
        }
    }


class Project(BaseModel):
    """Schema for project response"""
    id: str
    name: str
    project_type: ProjectType
    business_context: Optional[str]
    criticality_level: CriticalityLevel
    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "id": "550e8400-e29b-41d4-a716-446655440000",
                "name": "Production API Platform",
                "project_type": "cloud",
                "business_context": "SaaS API serving 100k users",
                "criticality_level": "high",
                "created_at": "2025-01-15T10:00:00Z",
                "updated_at": "2025-01-15T10:00:00Z"
            }
        }
    }


class ProjectList(BaseModel):
    """Schema for list of projects"""
    projects: list[Project]
    total: int

    model_config = {
        "json_schema_extra": {
            "example": {
                "projects": [
                    {
                        "id": "550e8400-e29b-41d4-a716-446655440000",
                        "name": "Production API Platform",
                        "project_type": "cloud",
                        "business_context": "SaaS API serving 100k users",
                        "criticality_level": "high",
                        "created_at": "2025-01-15T10:00:00Z",
                        "updated_at": "2025-01-15T10:00:00Z"
                    }
                ],
                "total": 1
            }
        }
    }
