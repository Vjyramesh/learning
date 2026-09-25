from fastapi import APIRouter
from app.modules.skills.schema import SkillCreate, SkillResponse, SkillUpdate, SkillId
from fastapi import Depends, Response
from app.modules.skills.services import SkillService
from app.modules.skills.repository import SkillRepository
from src.app.config.database import db_manager
from src.app.libs.response_utils import apply_response_headers
router = APIRouter(prefix='/skills', tags=['skills'])

def get_skill_services() -> SkillService:
    repository = SkillRepository(db = db_manager)
    return SkillService(repository)

@router.get("/")
async def get_all_skills(response: Response):
    service = get_skill_services()
    skills = await service.get_all_skills()
    apply_response_headers(response, skills)
    return skills


@router.post("/", response_model=SkillResponse)
async def create_skill(payload: SkillCreate, response: Response, service: SkillService = Depends(get_skill_services)):
    skill = await service.create(
        name=payload.name,
        category=payload.category,
        proficiency_level=payload.proficiency_level,
        years_of_experience=payload.years_of_experience,
        icon_name=payload.icon_name
    )
    apply_response_headers(response, skill)
    return skill

@router.put('/', response_model=SkillResponse)
async def update_skill(payload: SkillUpdate, response: Response, service: SkillService = Depends(get_skill_services)):
    id = payload.id
    data = payload.model_dump(exclude_unset=True, exclude={"id"})
    skill = await service.update(id, data)
    apply_response_headers(response, skill)
    return skill

@router.delete('/{id}', response_model=SkillResponse)
async def delete_skill(payload: SkillId, response: Response, service: SkillService = Depends(get_skill_services)):
    skill = await service.delete_by_id(payload.id)
    apply_response_headers(response, skill)
    return skill

@router.get('/{id}', response_model=SkillResponse)
async def get_skill_by_id(id: int, response: Response, service: SkillService = Depends(get_skill_services)):
    skill = await service.get_by_id(id)
    apply_response_headers(response, skill)
    return skill
