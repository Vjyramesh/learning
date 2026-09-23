from app.modules.basic_info.repository import BasicInfoRepository
from app.modules.basic_info.schema import BasicInfoResponse

class BasicInfoService:
    def __init__(self, repository: BasicInfoRepository):
        self.repository = repository

    async def fetch_basic_info(self):
        basic_info = await self.repository.get()
        if not basic_info:
            return None
        return BasicInfoResponse(**basic_info)