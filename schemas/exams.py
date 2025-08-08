from typing import Optional, List, Literal

from pydantic import BaseModel, Field

from common_primitives import Metadata
from question_hierarchy import Question
from sections import Group


class ExamBase(BaseModel):
    metadata: Optional[Metadata] = None
    title: Optional[str] = None
    instructions: Optional[str] = None
    duration_minutes: Optional[int] = None
    groups: List[Group] = Field(default_factory=list)
    questions: List[Question] = Field(default_factory=list)
    answer_key_complete: bool = False

class ObjectiveExam(ExamBase):
    exam_type: Literal["objective"] = "objective"

class SubjectiveExam(ExamBase):
    exam_type: Literal["subjective"] = "subjective"