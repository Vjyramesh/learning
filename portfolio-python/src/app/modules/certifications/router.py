
from fastapi import APIRouter, Depends, Response
from .repository import CertificationRepository
from .services import CertificationService
from src.app.config.database import db_manager
from .schema import CertificationResponse, CertificationCreate, CertificationUpdate

router = APIRouter(prefix='/certifications', tags=['certifications'])

def get_certifications_services():
    repository = CertificationRepository(db = db_manager)
    service = CertificationService(repository = repository)
    return service

def _apply_response_headers(response: Response, result: CertificationResponse):
    response.status_code = result.status
    response.headers["X-Success"] = str(result.success).lower()
    response.headers["X-Error"] = str(result.error).lower()

@router.get('/', response_model=CertificationResponse)
async def get_all_certifications(response: Response, service: CertificationService = Depends(get_certifications_services)):
    certifications = await service.get_all_certifications();
    _apply_response_headers(response, certifications)
    return certifications

@router.post('/', response_model=CertificationResponse)
async def create_certification(payload: CertificationCreate, response: Response, service: CertificationService = Depends(get_certifications_services)):
    certification = await service.create(
        name=payload.name,
        issuing_organization=payload.issuing_organization,
        issue_date=payload.issue_date,
        expiration_date=payload.expiration_date,
        credential_id=payload.credential_id,
        credential_url= str(payload.credential_url)
    )
    _apply_response_headers(response, certification)
    return certification

@router.put('/', response_model=CertificationResponse)
async def update_certification(payload: CertificationUpdate, response: Response, service: CertificationService = Depends(get_certifications_services)):
    certification = await service.update(
       id=payload.id,
       data={
           "name": payload.name,
           "issuing_organization": payload.issuing_organization,
           "issue_date": payload.issue_date,
           "expiration_date": payload.expiration_date,
           "credential_id": payload.credential_id,
           "credential_url": str(payload.credential_url)
       }
    )
    _apply_response_headers(response, certification)
    return certification