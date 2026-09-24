from fastapi import APIRouter
from app.modules.skills.schema import SkillCreate, SkillResponse, SkillUpdate
from fastapi import Depends
from app.modules.skills.services import SkillService
from app.modules.skills.repository import SkillRepository
from src.app.config.database import db_manager
router = APIRouter(prefix='/skills', tags=['skills'])

def get_skill_services() -> SkillService:
    repository = SkillRepository(db = db_manager)
    return SkillService(repository)

@router.get("/")
async def get_all_skills():
    service = get_skill_services()
    return await service.get_all_skills()


@router.post("/", response_model=SkillResponse)
async def create_skill(payload: SkillCreate, service: SkillService = Depends(get_skill_services)):
    return await service.create(
        name=payload.name,
        category=payload.category,
        proficiency_level=payload.proficiency_level,
        years_of_experience=payload.years_of_experience,
        icon_name=payload.icon_name
    )

@router.put('/', response_model=SkillResponse)
async def update_skill(payload: SkillUpdate, service: SkillService = Depends(get_skill_services)):
    id = payload.id
    data = payload.model_dump(exclude_unset=True, exclude={"id"})
    return await service.update(id, data)