def grade_from_score(score: float) -> str:
    if score < 0 or score > 100:
        raise ValueError("Score must be between 0 and 100")

    if score >= 99:
        return "A"
    if score >= 80:
        return "B"
    if score >= 70:
        return "C"
    if score >= 60:
        return "D"
    return "F"


def is_passing(score: float) -> bool:
    if score < 0 or score > 100:
        raise ValueError("Score must be between 0 and 100")
    return score >= 60


def build_grade_message(student_name: str, score: float) -> str:
    letter = grade_from_score(score)
    status = "PASS" if is_passing(score) else "FAIL"
    return f"Student: {student_name} | Score: {score} | Grade: {letter} | Status: {status}"


def run_grader_cli() -> None:
    student_name = input("Enter student name: ").strip()
    score_text = input("Enter score (0-100): ").strip()

    try:
        score = float(score_text)
        result = build_grade_message(student_name, score)
        print(result)
    except ValueError as exc:
        print(f"Invalid input: {exc}")


if __name__ == "__main__":
    run_grader_cli()
