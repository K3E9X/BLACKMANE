"""API endpoints for project analyses and findings"""

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from database.connection import get_db
from repositories.analysis_repository import AnalysisRepository
from services.analysis_service import AnalysisService
from models.analysis import Analysis, FindingList

router = APIRouter()


def get_analysis_service(db: Session = Depends(get_db)) -> AnalysisService:
    """Dependency injection for AnalysisService"""
    repository = AnalysisRepository(db)
    return AnalysisService(repository)


@router.post(
    "/projects/{project_id}/analyze",
    response_model=Analysis,
    status_code=status.HTTP_201_CREATED,
    summary="Run security analysis for a project",
)
def run_analysis(
    project_id: str,
    service: AnalysisService = Depends(get_analysis_service),
):
    """Run analysis on project's architecture"""
    return service.run_analysis(project_id)


@router.get(
    "/projects/{project_id}/analysis/latest",
    response_model=Analysis,
    summary="Get latest analysis for a project",
)
def get_latest_analysis(
    project_id: str,
    service: AnalysisService = Depends(get_analysis_service),
):
    """Get latest analysis for project"""
    return service.get_latest_analysis(project_id)


@router.get(
    "/projects/{project_id}/findings",
    response_model=FindingList,
    summary="Get findings from latest analysis",
)
def get_project_findings(
    project_id: str,
    service: AnalysisService = Depends(get_analysis_service),
):
    """Get findings from latest analysis for project"""
    return service.get_findings_for_project(project_id)
