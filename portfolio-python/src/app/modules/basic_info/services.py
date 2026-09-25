from app.modules.basic_info.repository import BasicInfoRepository
from app.modules.basic_info.schema import BasicInfoResponse, BasicInfoData

class BasicInfoService:
    def __init__(self, repository: BasicInfoRepository):
        self.repository = repository

    async def fetch_basic_info(self):
        """ Fetch the basic information from the repository.

        Returns:
            BasicInfoResponse: The response containing the basic information if found, otherwise an error message.
        """
        basic_info = await self.repository.get()
        if not basic_info:
            return BasicInfoResponse(success=False, message="Basic info not found", status=404, data=None)
        return BasicInfoResponse(success=True, message="Basic info fetched successfully", status=200, data=BasicInfoData(**basic_info))

    async def create_basic_info(self, name, email, phone, bio, about_me, github_url, linkedin_url, website_url, avatar_url, favicon_url):
        basic_info = await self.repository.create(name, email, phone, bio, about_me, github_url, linkedin_url, website_url, avatar_url, favicon_url)
        if not basic_info:
            return BasicInfoResponse(success=False, message="Failed to create basic info", status=400, data=None)
        return BasicInfoResponse(success=True, message="Basic info created successfully", status=201, data=BasicInfoData(**basic_info))

    async def update_basic_info(self, id, data):
        basic_info = await self.repository.update(id, data)
        if not basic_info:
            return BasicInfoResponse(success=False, message="Failed to update basic info or record not found", status=404, data=None)
        return BasicInfoResponse(success=True, message="Basic info updated successfully", status=200, data=BasicInfoData(**basic_info))

    async def delete_basic_info(self, id):
        basic_info = await self.repository.delete(id)
        if not basic_info:
            return BasicInfoResponse(success=False, message="Failed to delete basic info or record not found", status=404, data=None)
        return BasicInfoResponse(success=True, message="Basic info deleted successfully", status=200, data=None)