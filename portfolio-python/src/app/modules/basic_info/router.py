from fastapi import APIRouter, Depends, HTTPException, status
from src.app.modules.basic_info.schema import BasicInfoResponse, BasicInfoCreate, BasicInfoUpdate, BasicInfoDelete
from src.app.modules.basic_info.services import BasicInfoService
from src.app.modules.basic_info.repository import BasicInfoRepository
from src.app.config.database import db_manager

router = APIRouter(prefix="/basic-info", tags=["Basic Info"])

""" This module contains the API endpoints for managing basic information. """


def get_basic_info_service() -> BasicInfoService:
    """ Get the database-backed basic info service instance.
    Args:
        None
    Returns:
        BasicInfoService: The service instance for managing basic info.
    """
    repository = BasicInfoRepository(db=db_manager)
    return BasicInfoService(repository=repository)


@router.get("", response_model = BasicInfoResponse)
async def fetch_basic_info(service: BasicInfoService = Depends(get_basic_info_service)):
    """ API endpoint to fetch basic information 
        Args:
            service (BasicInfoService): The service instance for managing basic info.
        Returns:
            BasicInfoResponse: The response containing the basic information.
        
        Raises:
            HTTPException: If the basic information is not found.
    """
    profile = await service.fetch_basic_info()

    if not profile.success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"error": True, "message": "Data not found"})
    return profile

@router.post("", response_model=BasicInfoResponse)
async def create_basic_info(
    payload: BasicInfoCreate,
    service: BasicInfoService = Depends(get_basic_info_service)
):
    """ API endpoint to create basic information 
        Args:
            payload (BasicInfoCreate): The payload containing the basic information to create.
            service (BasicInfoService): The service instance for managing basic info.
        Returns:
            BasicInfoResponse: The response containing the created basic information.
        
        Raises:
            HTTPException: If the creation of basic information fails.
    """
    create = await service.create_basic_info(
        name=payload.name,
        email=payload.email,
        phone=payload.phone,
        bio=payload.bio,
        about_me=payload.about_me,
        github_url= str(payload.github_url),
        linkedin_url= str(payload.linkedin_url),
        website_url= str(payload.website_url),
        avatar_url= str(payload.avatar_url),
        favicon_url= str(payload.favicon_url)
    )

    if not create.success:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={"error": True, "data": create.model_dump()})
    return create

@router.put("", response_model=BasicInfoResponse)
async def update_basic_info(payload: BasicInfoUpdate, service: BasicInfoService = Depends(get_basic_info_service)):
    """ API endpoint to update basic information 
        Args:
            payload (BasicInfoUpdate): The payload containing the basic information to update.
            service (BasicInfoService): The service instance for managing basic info.
        Returns:
            BasicInfoResponse: The response containing the updated basic information.
        
        Raises:
            HTTPException: If the update of basic information fails or no data is provided.
    """
    update_data = payload.model_dump(exclude_unset=True, exclude={"id"})
    for key, value in update_data.items():
        if value is not None and key.endswith("_url"):
            update_data[key] = str(value)
    if not update_data:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={"error": True, "message": "No data provided for update"})

    update = await service.update_basic_info(id = payload.id, data = update_data)

    if not update.success:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={"error": True, "message": "Failed to update basic info or record not found"})
    return update

@router.delete("", response_model=BasicInfoResponse)
async def delete_basic_info(payload: BasicInfoDelete, service: BasicInfoService = Depends(get_basic_info_service)):
    """ API endpoint to delete basic information 
        Args:
            payload (BasicInfoDelete): The payload containing the ID of the basic information to delete.
            service (BasicInfoService): The service instance for managing basic info.
        Returns:
            BasicInfoResponse: The response containing the deleted basic information.
        
        Raises:
            HTTPException: If the deletion of basic information fails or the record is not found.
    """
    delete = await service.delete_basic_info(id=payload.id)

    if not delete.success:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={"error": True, "message": "Failed to delete basic info or record not found"})
    return delete
