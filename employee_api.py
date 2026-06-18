from typing import Any

from fastapi import APIRouter, HTTPException, Response, status

from bug_employee_store import Employee, EmployeeCreate, EmployeeUpdate, bugs_db, employees_db, get_next_employee_id

router = APIRouter(prefix="/employees", tags=["employees"])


@router.get("", response_model=list[Employee])
def list_employees() -> list[Employee]:
    return list(employees_db.values())


@router.get("/{employee_id}", response_model=Employee)
def get_employee(employee_id: int) -> Employee:
    employee = employees_db.get(employee_id)
    if not employee:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found")
    return employee


@router.post("", response_model=Employee, status_code=status.HTTP_201_CREATED)
def create_employee(payload: EmployeeCreate) -> Employee:
    employee_id = get_next_employee_id()
    employee = Employee(id=employee_id, **payload.model_dump())
    employees_db[employee_id] = employee
    return employee


@router.put("/{employee_id}", response_model=Employee)
def replace_employee(employee_id: int, payload: EmployeeCreate) -> Employee:
    if employee_id not in employees_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found")

    updated_employee = Employee(id=employee_id, **payload.model_dump())
    employees_db[employee_id] = updated_employee
    return updated_employee


@router.patch("/{employee_id}", response_model=Employee)
def update_employee(employee_id: int, payload: EmployeeUpdate) -> Employee:
    existing = employees_db.get(employee_id)
    if not existing:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found")

    patch_data: dict[str, Any] = payload.model_dump(exclude_unset=True)
    merged = existing.model_copy(update=patch_data)
    employees_db[employee_id] = merged
    return merged


@router.delete("/{employee_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_employee(employee_id: int) -> Response:
    if employee_id not in employees_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found")

    # Unassign deleted employee from bugs to keep references valid.
    for bug_id, bug in bugs_db.items():
        if bug.assigned_to_employee_id == employee_id:
            bugs_db[bug_id] = bug.model_copy(update={"assigned_to_employee_id": None})

    del employees_db[employee_id]
    return Response(status_code=status.HTTP_204_NO_CONTENT)
