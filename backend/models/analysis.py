"""
Pydantic models for Analysis and Finding entities
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class Finding(BaseModel):
    """Schema for finding response"""
    id: str
    analysis_id: str
    rule_id: str
    rule_name: str
    category: str
    severity: str
    title: str
    description: str
    impact: str
    affected_component_id: Optional[str] = None
    affected_flow_id: Optional[str] = None
    created_at: datetime

    model_config = {
        "from_attributes": True,
    }


class FindingList(BaseModel):
    """Schema for list of findings"""
    findings: list[Finding]
    total: int


class Analysis(BaseModel):
    """Schema for analysis response"""
    id: str
    project_id: str
    status: str
    started_at: datetime
    completed_at: Optional[datetime] = None
    global_risk_score: Optional[float] = None
    total_findings: int = Field(0, ge=0)
    critical_findings: int = Field(0, ge=0)
    high_findings: int = Field(0, ge=0)
    medium_findings: int = Field(0, ge=0)
    low_findings: int = Field(0, ge=0)

    model_config = {
        "from_attributes": True,
    }
