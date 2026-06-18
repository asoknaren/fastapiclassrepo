from typing import Any

from fastapi import APIRouter, HTTPException, Response, status

from bug_employee_store import Bug, BugCreate, BugUpdate, bugs_db, employees_db, get_next_bug_id

router = APIRouter(prefix="/bugs", tags=["bugs"])


def _validate_employee_references(created_by_employee_id: int | None, assigned_to_employee_id: int | None) -> None:
    if created_by_employee_id is not None and created_by_employee_id not in employees_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="created_by_employee_id does not exist",
        )

    if assigned_to_employee_id is not None and assigned_to_employee_id not in employees_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="assigned_to_employee_id does not exist",
        )


@router.get("", response_model=list[Bug])
def list_bugs() -> list[Bug]:
    return list(bugs_db.values())


@router.get("/{bug_id}", response_model=Bug)
def get_bug(bug_id: int) -> Bug:
    bug = bugs_db.get(bug_id)
    if not bug:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Bug not found")
    return bug


@router.post("", response_model=Bug, status_code=status.HTTP_201_CREATED)
def create_bug(payload: BugCreate) -> Bug:
    _validate_employee_references(payload.created_by_employee_id, payload.assigned_to_employee_id)

    bug_id = get_next_bug_id()
    bug = Bug(id=bug_id, **payload.model_dump())
    bugs_db[bug_id] = bug
    return bug


@router.put("/{bug_id}", response_model=Bug)
def replace_bug(bug_id: int, payload: BugCreate) -> Bug:
    if bug_id not in bugs_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Bug not found")

    _validate_employee_references(payload.created_by_employee_id, payload.assigned_to_employee_id)

    updated_bug = Bug(id=bug_id, **payload.model_dump())
    bugs_db[bug_id] = updated_bug
    return updated_bug


@router.patch("/{bug_id}", response_model=Bug)
def update_bug(bug_id: int, payload: BugUpdate) -> Bug:
    existing = bugs_db.get(bug_id)
    if not existing:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Bug not found")

    patch_data: dict[str, Any] = payload.model_dump(exclude_unset=True)

    _validate_employee_references(
        patch_data.get("created_by_employee_id"),
        patch_data.get("assigned_to_employee_id"),
    )

    merged_data = existing.model_dump()
    merged_data.update(patch_data)
    merged = Bug(**merged_data)

    bugs_db[bug_id] = merged
    return merged


@router.delete("/{bug_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_bug(bug_id: int) -> Response:
    if bug_id not in bugs_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Bug not found")

    del bugs_db[bug_id]
    return Response(status_code=status.HTTP_204_NO_CONTENT)
