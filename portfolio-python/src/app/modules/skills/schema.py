
import datetime
from pydantic import BaseModel
from typing import List, Optional, Union


class SkillBase(BaseModel):
    name: str
    category: str
    proficiency_level: str
    years_of_experience: int
    icon_name: str


class SkillCreate(SkillBase):
    pass

class SkillData(SkillBase):
    id: int
    created_at: datetime.datetime
    updated_at: datetime.datetime

class SkillId(BaseModel):
    id: int

class SkillResponse(BaseModel):
    success: bool
    message: str
    error: bool = False
    data: Optional[Union[SkillData, List[SkillData]]] = None

class SkillUpdate(SkillId):
    name: Optional[str] = None
    category: Optional[str] = None
    proficiency_level: Optional[str] = None
    years_of_experience: Optional[int] = None
    icon_name: Optional[str] = None