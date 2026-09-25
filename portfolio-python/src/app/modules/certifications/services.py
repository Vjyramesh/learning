from .repository import CertificationRepository
from .schema import CertificationResponse
class CertificationService:
    def __init__(self, repository: CertificationRepository):
        self.repository = repository

    async def get_all_certifications(self):
        certifications = await self.repository.get_all()
        if not certifications:
            return CertificationResponse(
                message="No certifications found",
                data=None,
                error=True,
                status=404,
                success=False
            )
        return CertificationResponse(
            message="Fetched all certifications",
            data=certifications,
            error=False,
            status=200,
            success=True
        )

    async def create(self, name, issuing_organization, issue_date, expiration_date=None, credential_id=None, credential_url=None):
        certification = await self.repository.create_certification(name, issuing_organization, issue_date, expiration_date, credential_id, credential_url)
        if not certification:
            return CertificationResponse(
                message="Failed to create certification",
                data=None,
                error=True,
                status=400,
                success=False
            )
        return CertificationResponse(
            message="Certification created successfully",
            data=certification,
            error=False,
            status=201,
            success=True
        )

    async def update(self, id, data):
        certification = await self.repository.update_certification(id, data)
        if not certification:
            return CertificationResponse(
                message="Failed to update certification",
                data=None,
                error=True,
                status=404,
                success=False
            )
        return CertificationResponse(
            message="Certification updated successfully",
            data=certification,
            status=200,
            error=False,
            success=True
        )