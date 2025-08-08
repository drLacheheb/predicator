from typing import Optional, List

from pydantic import BaseModel, Field

from schemas.common_primitives import SharedContext
from schemas.question_hierarchy import Question


class Group(BaseModel):
    id: Optional[str] = None
    title: Optional[str] = None
    shared_context: Optional[SharedContext] = None
    instructions: Optional[str] = None
    questions: List[Question] = Field(default_factory=list)