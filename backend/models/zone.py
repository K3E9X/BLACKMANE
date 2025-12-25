"""
Pydantic models for Zone entity
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field
from enum import Enum


class TrustLevel(str, Enum):
    """Trust levels for zones"""
    UNTRUSTED = "untrusted"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class ZoneCreate(BaseModel):
    """Schema for creating a zone"""
    architecture_id: str = Field(..., min_length=36, max_length=36, description="Architecture ID")
    name: str = Field(..., min_length=1, max_length=100, description="Zone name")
    trust_level: TrustLevel = Field(..., description="Trust level of the zone")
    description: Optional[str] = Field(None, description="Zone description")

    model_config = {
        "json_schema_extra": {
            "examples": [{
                "architecture_id": "123e4567-e89b-12d3-a456-426614174000",
                "name": "DMZ",
                "trust_level": "low",
                "description": "Demilitarized zone for public-facing services"
            }]
        }
    }


class ZoneUpdate(BaseModel):
    """Schema for updating a zone"""
    name: Optional[str] = Field(None, min_length=1, max_length=100, description="Zone name")
    trust_level: Optional[TrustLevel] = Field(None, description="Trust level of the zone")
    description: Optional[str] = Field(None, description="Zone description")

    model_config = {
        "json_schema_extra": {
            "examples": [{
                "name": "DMZ - Updated",
                "trust_level": "medium",
                "description": "Updated description"
            }]
        }
    }


class Zone(BaseModel):
    """Schema for zone response"""
    id: str
    architecture_id: str
    name: str
    trust_level: TrustLevel
    description: Optional[str] = None
    created_at: datetime

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "examples": [{
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "architecture_id": "123e4567-e89b-12d3-a456-426614174001",
                "name": "DMZ",
                "trust_level": "low",
                "description": "Demilitarized zone",
                "created_at": "2025-12-25T10:00:00"
            }]
        }
    }


class ZoneList(BaseModel):
    """Schema for listing zones"""
    zones: list[Zone]
    total: int

    model_config = {
        "json_schema_extra": {
            "examples": [{
                "zones": [],
                "total": 0
            }]
        }
    }
