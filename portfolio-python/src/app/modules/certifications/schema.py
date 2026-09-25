
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, HttpUrl


class CertificationBase(BaseModel):
    name: str
    issuing_organization: str
    issue_date: datetime
    expiration_date: datetime | None = None
    credential_id: str | None = None
    credential_url: HttpUrl | None = None

class CertificationCreate(CertificationBase):
    pass

class CertificationData(CertificationBase):
    id: int

class CertificationResponse(BaseModel):
    message: str
    data: CertificationData | None = None
    error: bool
    status: int
    success: bool

class CertificationUpdate(CertificationData):
    name: Optional[str] = None
    issuing_organization: Optional[str] = None
    issue_date: Optional[datetime] = None
    expiration_date: Optional[datetime] = None
    credential_id: Optional[str] = None
    credential_url: Optional[HttpUrl] = None
