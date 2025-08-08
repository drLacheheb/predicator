from fastapi import APIRouter, UploadFile, File, HTTPException

from schemas.exams import Exam
from services.extract import exam_to_object

exams_router = APIRouter()


@exams_router.post(
    "/parse",
    response_model=Exam,
    summary="Parse an exam PDF into normalized JSON",
)
async def parse_exam_pdf(file: UploadFile = File(..., media_type="application/pdf")) -> Exam:
    if file.content_type not in ("application/pdf",):
        raise HTTPException(status_code=415, detail="Only PDF files are supported.")

    data = await file.read()
    if not data:
        raise HTTPException(status_code=400, detail="Empty file.")

    try:
        exam = await exam_to_object(data)
    except Exception as e:
        raise HTTPException(status_code=422, detail=f"Failed to parse exam PDF: {e}")

    return exam
