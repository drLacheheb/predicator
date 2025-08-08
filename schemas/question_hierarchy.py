from typing import Literal, Optional, List, Union, Dict

from pydantic import BaseModel, Field

from schemas.common_primitives import SharedContext
from schemas.answer_primitives import ChoiceOption, MatchPair, BlankSpec

QuestionKind = Literal[
    "multiple_choice",
    "true_false",
    "matching",
    "fill_in_blank",
    "short_answer",
    "essay",
    "open_ended",
    "computational",
    "case_study",
]

class BaseQuestion(BaseModel):
    kind: QuestionKind
    id: Optional[str] = None
    prompt: str
    shared_context: Optional[SharedContext] = None
    difficulty: Optional[Literal["easy", "medium", "hard"]] = None
    learning_objectives: List[str] = Field(default_factory=list)

class MultipleChoiceQuestion(BaseQuestion):
    kind: Literal["multiple_choice"] = "multiple_choice"
    options: List[ChoiceOption]
    multiple_select: bool = False
    shuffle_options: bool = True
    rationale: Optional[str] = None

class TrueFalseQuestion(BaseQuestion):
    kind: Literal["true_false"] = "true_false"
    answer: Optional[bool] = None
    feedback_true: Optional[str] = None
    feedback_false: Optional[str] = None
    rationale: Optional[str] = None

class MatchingQuestion(BaseQuestion):
    kind: Literal["matching"] = "matching"
    pairs: List[MatchPair]
    shuffle_right_column: bool = True
    rationale: Optional[str] = None

class FillBlankQuestion(BaseQuestion):
    kind: Literal["fill_in_blank"] = "fill_in_blank"
    text_with_blanks: str
    blanks: List[BlankSpec]
    rationale: Optional[str] = None

class ShortAnswerQuestion(BaseQuestion):
    kind: Literal["short_answer"] = "short_answer"
    expected_keywords: List[str] = Field(default_factory=list)
    sample_answer: Optional[str] = None

class EssayQuestion(BaseQuestion):
    kind: Literal["essay"] = "essay"
    min_words: Optional[int] = None
    max_words: Optional[int] = None
    outline_points: List[str] = Field(default_factory=list)

class OpenEndedQuestion(BaseQuestion):
    kind: Literal["open_ended"] = "open_ended"
    response_format: Optional[Literal["text", "code", "diagram"]] = "text"
    sample_answer: Optional[str] = None

class ComputationalSubpart(BaseModel):
    id: Optional[str] = None
    prompt: str
    answer: Optional[str] = None
    solution_steps: List[str] = Field(default_factory=list)

class ComputationalQuestion(BaseQuestion):
    kind: Literal["computational"] = "computational"
    givens: Dict[str, Union[int, float, str]] = Field(default_factory=dict)
    variables: List[str] = Field(default_factory=list)
    sub_parts: List[ComputationalSubpart] = Field(default_factory=list)
    final_answer: Optional[str] = None
    units: Optional[str] = None
    rationale: Optional[str] = None

class CaseStudyQuestion(BaseQuestion):
    kind: Literal["case_study"] = "case_study"
    case: SharedContext
    subquestions: List[Union[
        MultipleChoiceQuestion,
        TrueFalseQuestion,
        ShortAnswerQuestion,
        OpenEndedQuestion,
        ComputationalQuestion,
        FillBlankQuestion,
        MatchingQuestion,
        EssayQuestion
    ]] = Field(default_factory=list)

Question = Union[
    MultipleChoiceQuestion,
    TrueFalseQuestion,
    MatchingQuestion,
    FillBlankQuestion,
    ShortAnswerQuestion,
    EssayQuestion,
    OpenEndedQuestion,
    ComputationalQuestion,
    CaseStudyQuestion,
]