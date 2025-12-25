"""
SQLAlchemy ORM Models for BLACKMANE

Database models for all entities
"""

from datetime import datetime
from sqlalchemy import Column, String, Text, Integer, Boolean, Float, DateTime, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
import enum

from database.connection import Base


# Enums
class ProjectTypeEnum(str, enum.Enum):
    CLOUD = "cloud"
    ON_PREMISE = "on-premise"
    HYBRID = "hybrid"


class CriticalityLevelEnum(str, enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class TrustLevelEnum(str, enum.Enum):
    UNTRUSTED = "untrusted"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class ComponentTypeEnum(str, enum.Enum):
    FIREWALL = "firewall"
    LOAD_BALANCER = "load_balancer"
    SERVER = "server"
    DATABASE = "database"
    IAM = "iam"
    BASTION = "bastion"
    API_GATEWAY = "api_gateway"
    VPN = "vpn"
    OTHER = "other"


class FlowProtocolEnum(str, enum.Enum):
    HTTP = "http"
    HTTPS = "https"
    SSH = "ssh"
    RDP = "rdp"
    SQL = "sql"
    LDAP = "ldap"
    DNS = "dns"
    SMTP = "smtp"
    OTHER = "other"


# Models
class Project(Base):
    """Project model - represents an architecture analysis project"""
    __tablename__ = "projects"

    id = Column(String(36), primary_key=True)
    name = Column(String(200), nullable=False)
    project_type = Column(SQLEnum(ProjectTypeEnum), nullable=False)
    business_context = Column(Text, nullable=True)
    criticality_level = Column(SQLEnum(CriticalityLevelEnum), nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    architecture = relationship("Architecture", back_populates="project", uselist=False, cascade="all, delete-orphan")
    analyses = relationship("Analysis", back_populates="project", cascade="all, delete-orphan")


class Architecture(Base):
    """Architecture model - represents the architecture being analyzed"""
    __tablename__ = "architectures"

    id = Column(String(36), primary_key=True)
    project_id = Column(String(36), ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, unique=True)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    project = relationship("Project", back_populates="architecture")
    zones = relationship("Zone", back_populates="architecture", cascade="all, delete-orphan")
    components = relationship("Component", back_populates="architecture", cascade="all, delete-orphan")
    flows = relationship("Flow", back_populates="architecture", cascade="all, delete-orphan")


class Zone(Base):
    """Zone model - trust zones in the architecture"""
    __tablename__ = "zones"

    id = Column(String(36), primary_key=True)
    architecture_id = Column(String(36), ForeignKey("architectures.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(100), nullable=False)
    trust_level = Column(SQLEnum(TrustLevelEnum), nullable=False)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    # Relationships
    architecture = relationship("Architecture", back_populates="zones")
    components = relationship("Component", back_populates="zone", cascade="all, delete-orphan")


class Component(Base):
    """Component model - components in the architecture"""
    __tablename__ = "components"

    id = Column(String(36), primary_key=True)
    architecture_id = Column(String(36), ForeignKey("architectures.id", ondelete="CASCADE"), nullable=False)
    zone_id = Column(String(36), ForeignKey("zones.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(100), nullable=False)
    component_type = Column(SQLEnum(ComponentTypeEnum), nullable=False)
    has_admin_interface = Column(Boolean, nullable=False, default=False)
    requires_mfa = Column(Boolean, nullable=False, default=False)
    has_logging = Column(Boolean, nullable=False, default=False)
    encryption_at_rest = Column(Boolean, nullable=False, default=False)
    encryption_in_transit = Column(Boolean, nullable=False, default=False)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    # Relationships
    architecture = relationship("Architecture", back_populates="components")
    zone = relationship("Zone", back_populates="components")
    flows_as_source = relationship("Flow", foreign_keys="Flow.source_component_id", back_populates="source_component", cascade="all, delete-orphan")
    flows_as_target = relationship("Flow", foreign_keys="Flow.target_component_id", back_populates="target_component", cascade="all, delete-orphan")


class Flow(Base):
    """Flow model - data flows between components"""
    __tablename__ = "flows"

    id = Column(String(36), primary_key=True)
    architecture_id = Column(String(36), ForeignKey("architectures.id", ondelete="CASCADE"), nullable=False)
    source_component_id = Column(String(36), ForeignKey("components.id", ondelete="CASCADE"), nullable=False)
    target_component_id = Column(String(36), ForeignKey("components.id", ondelete="CASCADE"), nullable=False)
    protocol = Column(SQLEnum(FlowProtocolEnum), nullable=False)
    port = Column(Integer, nullable=True)
    is_authenticated = Column(Boolean, nullable=False, default=False)
    is_encrypted = Column(Boolean, nullable=False, default=False)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    # Relationships
    architecture = relationship("Architecture", back_populates="flows")
    source_component = relationship("Component", foreign_keys=[source_component_id], back_populates="flows_as_source")
    target_component = relationship("Component", foreign_keys=[target_component_id], back_populates="flows_as_target")


class Analysis(Base):
    """Analysis model - security analysis results"""
    __tablename__ = "analyses"

    id = Column(String(36), primary_key=True)
    project_id = Column(String(36), ForeignKey("projects.id", ondelete="CASCADE"), nullable=False)
    status = Column(String(20), nullable=False, default="pending")  # pending, running, completed, failed
    started_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
    global_risk_score = Column(Float, nullable=True)
    total_findings = Column(Integer, nullable=False, default=0)
    critical_findings = Column(Integer, nullable=False, default=0)
    high_findings = Column(Integer, nullable=False, default=0)
    medium_findings = Column(Integer, nullable=False, default=0)
    low_findings = Column(Integer, nullable=False, default=0)

    # Relationships
    project = relationship("Project", back_populates="analyses")
    findings = relationship("Finding", back_populates="analysis", cascade="all, delete-orphan")
    maturity_assessments = relationship("MaturityAssessment", back_populates="analysis", cascade="all, delete-orphan")


class Finding(Base):
    """Finding model - security issues detected"""
    __tablename__ = "findings"

    id = Column(String(36), primary_key=True)
    analysis_id = Column(String(36), ForeignKey("analyses.id", ondelete="CASCADE"), nullable=False)
    rule_id = Column(String(50), nullable=False)
    rule_name = Column(String(200), nullable=False)
    category = Column(String(50), nullable=False)
    severity = Column(String(20), nullable=False)  # critical, high, medium, low
    title = Column(String(500), nullable=False)
    description = Column(Text, nullable=False)
    impact = Column(Text, nullable=False)
    affected_component_id = Column(String(36), ForeignKey("components.id", ondelete="SET NULL"), nullable=True)
    affected_flow_id = Column(String(36), ForeignKey("flows.id", ondelete="SET NULL"), nullable=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    # Relationships
    analysis = relationship("Analysis", back_populates="findings")
    recommendation = relationship("Recommendation", back_populates="finding", uselist=False, cascade="all, delete-orphan")


class Recommendation(Base):
    """Recommendation model - security recommendations"""
    __tablename__ = "recommendations"

    id = Column(String(36), primary_key=True)
    finding_id = Column(String(36), ForeignKey("findings.id", ondelete="CASCADE"), nullable=False)
    domain = Column(String(50), nullable=False)
    description = Column(Text, nullable=False)
    actions = Column(Text, nullable=False)  # JSON array stored as text
    priority = Column(String(20), nullable=False)  # critical, high, medium, low
    effort = Column(String(20), nullable=False)  # low, medium, high
    security_gain = Column(String(20), nullable=False)  # low, medium, high
    priority_score = Column(Float, nullable=False)
    status = Column(String(20), nullable=False, default="pending")  # pending, accepted, rejected, implemented
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    # Relationships
    finding = relationship("Finding", back_populates="recommendation")


class MaturityAssessment(Base):
    """Maturity assessment model - security maturity evaluation"""
    __tablename__ = "maturity_assessments"

    id = Column(String(36), primary_key=True)
    analysis_id = Column(String(36), ForeignKey("analyses.id", ondelete="CASCADE"), nullable=False)
    domain = Column(String(50), nullable=False)
    maturity_level = Column(Integer, nullable=False)  # 1-5
    score_percentage = Column(Float, nullable=False)
    total_rules = Column(Integer, nullable=False)
    passed_rules = Column(Integer, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    # Relationships
    analysis = relationship("Analysis", back_populates="maturity_assessments")
