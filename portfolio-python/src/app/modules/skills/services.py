from app.modules.skills.repository import SkillRepository
from app.modules.skills.schema import SkillData, SkillResponse
class SkillService:
    def __init__(self, repository: SkillRepository):
        self.repository = repository

    async def get_all_skills(self):
        if not self.repository:
            raise ValueError("Repository is not initialized")

        skills = await self.repository.get_all_skills()

        if not skills:
            return SkillResponse(success=True, message="No skills found", status=404, data=None)

        return SkillResponse(success=True, message="Skills retrieved successfully", status=200, data=[SkillData(**skill) for skill in skills])

    async def create(self, name: str, category: str, proficiency_level: str, years_of_experience: int, icon_name: str):
        if not self.repository:
            raise ValueError("Repository is not initialized")

        skill = await self.repository.create(name, category, proficiency_level, years_of_experience, icon_name)

        if not skill:
            return SkillResponse(success=False, message="Failed to create skill", status=400, data=None)

        return SkillResponse(success=True, message="Skill created successfully", status=201, data=SkillData(**skill))

    async def update(self, id: int, data:dict):
        if not self.repository:
            raise ValueError("Repository is not initialized")

        skill = await self.repository.update(id, data)

        if not skill:
            return SkillResponse(success=False, error=True, message="Failed to update skill", status=404, data=None)

        return SkillResponse(success=True, error=False, message="Skill updated successfully", status=200, data=SkillData(**skill))

    async def delete_by_id(self, id: int):
        if not self.repository:
            raise ValueError("Repository is not initialized")

        skill = await self.repository.delete_by_id(id)

        if not skill:
            return SkillResponse(success=False, error=True, message="Failed to delete skill", status=404, data=None)

        return SkillResponse(success=True, error=False, message="Skill deleted successfully", status=200, data=SkillData(**skill))

    async def get_by_id(self, id: int):
        if not self.repository:
            raise ValueError("Repository is not initialized")

        skill = await self.repository.get_by_id(id)

        if not skill:
            return SkillResponse(success=False, error=True, message="Skill not found", status=404, data=None)

        return SkillResponse(success=True, error=False, message="Skill retrieved successfully", status=200, data=SkillData(**skill))