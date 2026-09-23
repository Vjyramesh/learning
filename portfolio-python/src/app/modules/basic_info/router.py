from fastapi import APIRouter, Depends, HTTPException, status
from src.app.modules.basic_info.schema import BasicInfoResponse
from src.app.modules.basic_info.services import BasicInfoService
from src.app.modules.basic_info.repository import BasicInfoRepository
from src.app.config.database import db_manager

router = APIRouter(prefix="/basic-info", tags=["Basic Info"])

def get_basic_info_service() -> BasicInfoService:

    repository = BasicInfoRepository(db=db_manager)
    return BasicInfoService(repository=repository)

@router.get("", response_model = BasicInfoResponse)
async def fetch_basic_info(service: BasicInfoService = Depends(get_basic_info_service)):
    profile = await service.fetch_basic_info()

    if not profile:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Basic info not found")
    return profile