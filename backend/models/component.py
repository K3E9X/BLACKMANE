"""
Pydantic models for Component entity
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field
from enum import Enum


class ComponentType(str, Enum):
    """Component types"""
    FIREWALL = "firewall"
    LOAD_BALANCER = "load_balancer"
    SERVER = "server"
    DATABASE = "database"
    IAM = "iam"
    BASTION = "bastion"
    API_GATEWAY = "api_gateway"
    VPN = "vpn"
    OTHER = "other"


class ComponentCreate(BaseModel):
    """Schema for creating a component"""
    architecture_id: str = Field(..., min_length=36, max_length=36, description="Architecture ID")
    zone_id: str = Field(..., min_length=36, max_length=36, description="Zone ID")
    name: str = Field(..., min_length=1, max_length=100, description="Component name")
    component_type: ComponentType = Field(..., description="Type of component")
    has_admin_interface: bool = Field(default=False, description="Has admin interface")
    requires_mfa: bool = Field(default=False, description="Requires MFA")
    has_logging: bool = Field(default=False, description="Has logging enabled")
    encryption_at_rest: bool = Field(default=False, description="Encryption at rest")
    encryption_in_transit: bool = Field(default=False, description="Encryption in transit")
    description: Optional[str] = Field(None, description="Component description")

    model_config = {
        "json_schema_extra": {
            "examples": [{
                "architecture_id": "123e4567-e89b-12d3-a456-426614174000",
                "zone_id": "123e4567-e89b-12d3-a456-426614174001",
                "name": "Web Application Firewall",
                "component_type": "firewall",
                "has_admin_interface": True,
                "requires_mfa": True,
                "has_logging": True,
                "encryption_at_rest": False,
                "encryption_in_transit": True,
                "description": "Main WAF for public traffic"
            }]
        }
    }


class ComponentUpdate(BaseModel):
    """Schema for updating a component"""
    name: Optional[str] = Field(None, min_length=1, max_length=100, description="Component name")
    component_type: Optional[ComponentType] = Field(None, description="Type of component")
    zone_id: Optional[str] = Field(None, min_length=36, max_length=36, description="Zone ID")
    has_admin_interface: Optional[bool] = Field(None, description="Has admin interface")
    requires_mfa: Optional[bool] = Field(None, description="Requires MFA")
    has_logging: Optional[bool] = Field(None, description="Has logging enabled")
    encryption_at_rest: Optional[bool] = Field(None, description="Encryption at rest")
    encryption_in_transit: Optional[bool] = Field(None, description="Encryption in transit")
    description: Optional[str] = Field(None, description="Component description")

    model_config = {
        "json_schema_extra": {
            "examples": [{
                "name": "Updated WAF",
                "requires_mfa": True,
                "description": "Updated description"
            }]
        }
    }


class Component(BaseModel):
    """Schema for component response"""
    id: str
    architecture_id: str
    zone_id: str
    name: str
    component_type: ComponentType
    has_admin_interface: bool
    requires_mfa: bool
    has_logging: bool
    encryption_at_rest: bool
    encryption_in_transit: bool
    description: Optional[str] = None
    created_at: datetime

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "examples": [{
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "architecture_id": "123e4567-e89b-12d3-a456-426614174001",
                "zone_id": "123e4567-e89b-12d3-a456-426614174002",
                "name": "Web Application Firewall",
                "component_type": "firewall",
                "has_admin_interface": True,
                "requires_mfa": True,
                "has_logging": True,
                "encryption_at_rest": False,
                "encryption_in_transit": True,
                "description": "Main WAF",
                "created_at": "2025-12-25T10:00:00"
            }]
        }
    }


class ComponentList(BaseModel):
    """Schema for listing components"""
    components: list[Component]
    total: int

    model_config = {
        "json_schema_extra": {
            "examples": [{
                "components": [],
                "total": 0
            }]
        }
    }
