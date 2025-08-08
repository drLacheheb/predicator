from typing import Optional, List, Literal

from pydantic import BaseModel, Field

from schemas.common_primitives import Metadata
from schemas.question_hierarchy import Question
from schemas.sections import Group


class Exam(BaseModel):
    exam_type: Literal["objective", "subjective"]
    metadata: Optional[Metadata] = None
    title: Optional[str] = None
    instructions: Optional[str] = None
    duration_minutes: Optional[int] = None
    groups: List[Group] = Field(default_factory=list)
    questions: List[Question] = Field(default_factory=list)
    answer_key_complete: bool = False