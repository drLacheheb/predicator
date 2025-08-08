from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, Field


class SharedContext(BaseModel):
    title: Optional[str] = None
    text: Optional[str] = None
    language: Optional[str] = None

class Metadata(BaseModel):
    id: Optional[str] = None
    source: Optional[str] = None
    course: Optional[str] = None
    subject: Optional[str] = None
    grade_level: Optional[str] = None
    tags: List[str] = Field(default_factory=list)
    created_at: Optional[datetime] = None
    locale: Optional[str] = None