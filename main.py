from fastapi import FastAPI

from api.v1.endpoints.exam_analysis import exams_router

version = "v1"
app = FastAPI(
    title="Predicator",
    version=version,
)

app.include_router(exams_router, prefix=f"/api/{version}/exams", tags=["exams"])