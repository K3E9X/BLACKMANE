"""Analysis repository - data access for analyses and findings"""

from datetime import datetime
import uuid
from sqlalchemy.orm import Session

from models.orm import Analysis as AnalysisORM
from models.orm import Finding as FindingORM
from models.orm import Project as ProjectORM


class AnalysisRepository:
    """Repository for analysis persistence and queries"""

    def __init__(self, db: Session):
        self.db = db

    def get_project(self, project_id: str) -> ProjectORM | None:
        return self.db.query(ProjectORM).filter(ProjectORM.id == project_id).first()

    def create_analysis(self, project_id: str) -> AnalysisORM:
        analysis = AnalysisORM(
            id=str(uuid.uuid4()),
            project_id=project_id,
            status="running",
            started_at=datetime.utcnow(),
            total_findings=0,
            critical_findings=0,
            high_findings=0,
            medium_findings=0,
            low_findings=0,
        )
        self.db.add(analysis)
        self.db.commit()
        self.db.refresh(analysis)
        return analysis

    def add_finding(
        self,
        analysis_id: str,
        rule_id: str,
        rule_name: str,
        category: str,
        severity: str,
        title: str,
        description: str,
        impact: str,
        affected_component_id: str | None = None,
        affected_flow_id: str | None = None,
    ) -> FindingORM:
        finding = FindingORM(
            id=str(uuid.uuid4()),
            analysis_id=analysis_id,
            rule_id=rule_id,
            rule_name=rule_name,
            category=category,
            severity=severity,
            title=title,
            description=description,
            impact=impact,
            affected_component_id=affected_component_id,
            affected_flow_id=affected_flow_id,
        )
        self.db.add(finding)
        self.db.commit()
        self.db.refresh(finding)
        return finding

    def finalize_analysis(self, analysis_id: str) -> AnalysisORM | None:
        analysis = self.db.query(AnalysisORM).filter(AnalysisORM.id == analysis_id).first()
        if not analysis:
            return None

        findings = (
            self.db.query(FindingORM)
            .filter(FindingORM.analysis_id == analysis_id)
            .all()
        )

        critical_count = sum(1 for f in findings if f.severity == "critical")
        high_count = sum(1 for f in findings if f.severity == "high")
        medium_count = sum(1 for f in findings if f.severity == "medium")
        low_count = sum(1 for f in findings if f.severity == "low")

        analysis.total_findings = len(findings)
        analysis.critical_findings = critical_count
        analysis.high_findings = high_count
        analysis.medium_findings = medium_count
        analysis.low_findings = low_count
        analysis.global_risk_score = min(100.0, critical_count * 30 + high_count * 15 + medium_count * 7 + low_count * 3)
        analysis.status = "completed"
        analysis.completed_at = datetime.utcnow()

        self.db.commit()
        self.db.refresh(analysis)
        return analysis

    def get_latest_by_project(self, project_id: str) -> AnalysisORM | None:
        return (
            self.db.query(AnalysisORM)
            .filter(AnalysisORM.project_id == project_id)
            .order_by(AnalysisORM.started_at.desc())
            .first()
        )

    def get_findings_by_analysis(self, analysis_id: str) -> list[FindingORM]:
        return (
            self.db.query(FindingORM)
            .filter(FindingORM.analysis_id == analysis_id)
            .order_by(FindingORM.created_at.desc())
            .all()
        )
