
from pydantic import BaseModel, EmailStr, HttpUrl
from typing import Optional


class BasicInfoBase(BaseModel):
    name: str
    email: EmailStr
    phone: int
    bio: str
    about_me: str
    github_url: HttpUrl
    linkedin_url: HttpUrl
    website_url: HttpUrl
    avatar_url: str
    favicon_url: str

class BasicInfoData(BasicInfoBase):
    id: int

class BasicInfoCreate(BasicInfoBase):
    pass

class BasicInfoResponse(BaseModel):
    success: bool
    message: str
    error:Optional[str] = None
    status: int
    data: Optional[BasicInfoData] = None

class BasicInfoUpdate(BasicInfoData):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[int] = None
    bio: Optional[str] = None
    about_me: Optional[str] = None
    github_url: Optional[HttpUrl] = None
    linkedin_url: Optional[HttpUrl] = None
    website_url: Optional[HttpUrl] = None
    avatar_url: Optional[str] = None
    favicon_url: Optional[str] = None

class BasicInfoDelete(BaseModel):
    id: int