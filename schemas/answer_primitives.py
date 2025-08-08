from typing import Optional, List

from pydantic import BaseModel, Field


class ChoiceOption(BaseModel):
    id: str
    text: str
    is_correct: Optional[bool] = None
    feedback: Optional[str] = None

class BlankSpec(BaseModel):
    index: int
    acceptable_answers: List[str] = Field(default_factory=list)
    regex: Optional[str] = None
    case_sensitive: bool = False
    feedback: Optional[str] = None

class MatchPair(BaseModel):
    left: str
    right_correct: Optional[str] = None
    right_distractors: List[str] = Field(default_factory=list)