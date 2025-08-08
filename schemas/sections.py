from typing import Optional, List

from pydantic import BaseModel, Field

from common_primitives import SharedContext
from question_hierarchy import Question


class Group(BaseModel):
    id: Optional[str] = None
    title: Optional[str] = None
    stimulus: Optional[SharedContext] = None
    instructions: Optional[str] = None
    questions: List[Question] = Field(default_factory=list)