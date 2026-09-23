
from pydantic import BaseModel, EmailStr, HttpUrl


class BasicInfoBase(BaseModel):
    name: str
    email: EmailStr
    phone: str
    bio: str
    about_me: str
    github_url: HttpUrl
    linkedin_url: HttpUrl
    website_url: HttpUrl
    avatar_url: str
    favicon_url: str

class BasicInfoCreate(BasicInfoBase):
    pass

class BasicInfoResponse(BasicInfoBase):
    id: int