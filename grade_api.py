from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI(title="Class Grade Validation API")


class GradeInput(BaseModel):
    student_name: str = Field(..., min_length=1)
    course: str = Field(..., min_length=1)
    score: float = Field(..., ge=0, le=100)


class GradeValidationResult(BaseModel):
    student_name: str
    course: str
    score: float
    letter_grade: str
    passed: bool
    is_valid: bool


class BatchGradeInput(BaseModel):
    grades: list[GradeInput] = Field(..., min_length=1)


class BatchValidationResult(BaseModel):
    total_students: int
    pass_count: int
    fail_count: int
    results: list[GradeValidationResult]


def letter_grade_for_score(score: float) -> str:
    if score >= 90:
        return "A"
    if score >= 80:
        return "B"
    if score >= 70:
        return "C"
    if score >= 60:
        return "D"
    return "F"


def build_result(grade: GradeInput) -> GradeValidationResult:
    letter_grade = letter_grade_for_score(grade.score)
    passed = grade.score >= 60
    return GradeValidationResult(
        student_name=grade.student_name,
        course=grade.course,
        score=grade.score,
        letter_grade=letter_grade,
        passed=passed,
        is_valid=True,
    )


@app.get("/")
def root() -> dict[str, str]:
    return {"message": "Class Grade Validation API is running"}


@app.post("/grades/validate", response_model=GradeValidationResult)
def validate_grade(payload: GradeInput) -> GradeValidationResult:
    return build_result(payload)


@app.post("/grades/validate/batch", response_model=BatchValidationResult)
def validate_grade_batch(payload: BatchGradeInput) -> BatchValidationResult:
    results = [build_result(grade) for grade in payload.grades]
    pass_count = sum(1 for result in results if result.passed)
    fail_count = len(results) - pass_count

    return BatchValidationResult(
        total_students=len(results),
        pass_count=pass_count,
        fail_count=fail_count,
        results=results,
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8003)