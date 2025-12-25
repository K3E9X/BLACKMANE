"""
Pydantic models for Flow entity
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field
from enum import Enum


class FlowProtocol(str, Enum):
    """Flow protocols"""
    HTTP = "http"
    HTTPS = "https"
    SSH = "ssh"
    RDP = "rdp"
    SQL = "sql"
    LDAP = "ldap"
    DNS = "dns"
    SMTP = "smtp"
    OTHER = "other"


class FlowCreate(BaseModel):
    """Schema for creating a flow"""
    architecture_id: str = Field(..., min_length=36, max_length=36, description="Architecture ID")
    source_component_id: str = Field(..., min_length=36, max_length=36, description="Source component ID")
    target_component_id: str = Field(..., min_length=36, max_length=36, description="Target component ID")
    protocol: FlowProtocol = Field(..., description="Protocol used")
    port: Optional[int] = Field(None, ge=1, le=65535, description="Port number")
    is_authenticated: bool = Field(default=False, description="Flow is authenticated")
    is_encrypted: bool = Field(default=False, description="Flow is encrypted")
    description: Optional[str] = Field(None, description="Flow description")

    model_config = {
        "json_schema_extra": {
            "examples": [{
                "architecture_id": "123e4567-e89b-12d3-a456-426614174000",
                "source_component_id": "123e4567-e89b-12d3-a456-426614174001",
                "target_component_id": "123e4567-e89b-12d3-a456-426614174002",
                "protocol": "https",
                "port": 443,
                "is_authenticated": True,
                "is_encrypted": True,
                "description": "HTTPS traffic from web to API"
            }]
        }
    }


class FlowUpdate(BaseModel):
    """Schema for updating a flow"""
    protocol: Optional[FlowProtocol] = Field(None, description="Protocol used")
    port: Optional[int] = Field(None, ge=1, le=65535, description="Port number")
    is_authenticated: Optional[bool] = Field(None, description="Flow is authenticated")
    is_encrypted: Optional[bool] = Field(None, description="Flow is encrypted")
    description: Optional[str] = Field(None, description="Flow description")

    model_config = {
        "json_schema_extra": {
            "examples": [{
                "protocol": "https",
                "port": 8443,
                "is_encrypted": True,
                "description": "Updated description"
            }]
        }
    }


class Flow(BaseModel):
    """Schema for flow response"""
    id: str
    architecture_id: str
    source_component_id: str
    target_component_id: str
    protocol: FlowProtocol
    port: Optional[int] = None
    is_authenticated: bool
    is_encrypted: bool
    description: Optional[str] = None
    created_at: datetime

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "examples": [{
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "architecture_id": "123e4567-e89b-12d3-a456-426614174001",
                "source_component_id": "123e4567-e89b-12d3-a456-426614174002",
                "target_component_id": "123e4567-e89b-12d3-a456-426614174003",
                "protocol": "https",
                "port": 443,
                "is_authenticated": True,
                "is_encrypted": True,
                "description": "HTTPS traffic",
                "created_at": "2025-12-25T10:00:00"
            }]
        }
    }


class FlowList(BaseModel):
    """Schema for listing flows"""
    flows: list[Flow]
    total: int

    model_config = {
        "json_schema_extra": {
            "examples": [{
                "flows": [],
                "total": 0
            }]
        }
    }
