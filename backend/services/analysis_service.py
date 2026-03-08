"""Analysis service - security checks and findings generation"""

from fastapi import HTTPException, status

from repositories.analysis_repository import AnalysisRepository
from models.analysis import Analysis, Finding, FindingList
from models.orm import ComponentTypeEnum


class AnalysisService:
    """Service for architecture analysis"""

    def __init__(self, repository: AnalysisRepository):
        self.repository = repository

    def run_analysis(self, project_id: str) -> Analysis:
        project = self.repository.get_project(project_id)
        if not project:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Project {project_id} not found",
            )

        if not project.architecture:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Project has no architecture to analyze",
            )

        analysis = self.repository.create_analysis(project_id)

        for component in project.architecture.components:
            if component.has_admin_interface and not component.requires_mfa:
                self.repository.add_finding(
                    analysis_id=analysis.id,
                    rule_id="SEC-001",
                    rule_name="Admin interface requires MFA",
                    category="identity",
                    severity="high",
                    title=f"{component.name} has admin access without MFA",
                    description="Component exposes an admin interface but does not enforce MFA.",
                    impact="Account takeover risk is increased for privileged access paths.",
                    affected_component_id=component.id,
                )

            if component.component_type == ComponentTypeEnum.DATABASE and not component.encryption_at_rest:
                self.repository.add_finding(
                    analysis_id=analysis.id,
                    rule_id="SEC-011",
                    rule_name="Database encryption at rest",
                    category="data",
                    severity="critical",
                    title=f"Database {component.name} is not encrypted at rest",
                    description="Database component stores data without encryption at rest.",
                    impact="Sensitive data disclosure risk in case of storage compromise.",
                    affected_component_id=component.id,
                )

        for flow in project.architecture.flows:
            if flow.protocol in ["http", "sql"] and not flow.is_encrypted:
                self.repository.add_finding(
                    analysis_id=analysis.id,
                    rule_id="SEC-013",
                    rule_name="Sensitive flow must be encrypted",
                    category="network",
                    severity="medium",
                    title=f"Unencrypted flow {flow.source_component_id} → {flow.target_component_id}",
                    description="Data flow uses an insecure/non-encrypted protocol configuration.",
                    impact="Traffic interception or manipulation is possible on this communication path.",
                    affected_flow_id=flow.id,
                )

        finalized = self.repository.finalize_analysis(analysis.id)
        return Analysis.model_validate(finalized)

    def get_latest_analysis(self, project_id: str) -> Analysis:
        analysis = self.repository.get_latest_by_project(project_id)
        if not analysis:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No analysis found for project {project_id}",
            )
        return Analysis.model_validate(analysis)

    def get_findings_for_project(self, project_id: str) -> FindingList:
        latest = self.repository.get_latest_by_project(project_id)
        if not latest:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No analysis found for project {project_id}",
            )

        findings = self.repository.get_findings_by_analysis(latest.id)
        return FindingList(
            findings=[Finding.model_validate(f) for f in findings],
            total=len(findings),
        )
