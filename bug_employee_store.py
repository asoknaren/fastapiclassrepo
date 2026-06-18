from itertools import count
from typing import Literal

from pydantic import BaseModel, Field


class Employee(BaseModel):
    id: int = Field(..., gt=0)
    name: str = Field(..., min_length=1)
    email: str = Field(..., min_length=3)
    role: Literal["developer", "tester", "manager"]
    active: bool = True


class EmployeeCreate(BaseModel):
    name: str = Field(..., min_length=1)
    email: str = Field(..., min_length=3)
    role: Literal["developer", "tester", "manager"]
    active: bool = True


class EmployeeUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1)
    email: str | None = Field(default=None, min_length=3)
    role: Literal["developer", "tester", "manager"] | None = None
    active: bool | None = None


class Bug(BaseModel):
    id: int = Field(..., gt=0)
    title: str = Field(..., min_length=1)
    description: str = Field(..., min_length=1)
    priority: Literal["low", "medium", "high", "critical"]
    status: Literal["open", "in_progress", "resolved", "closed"] = "open"
    created_by_employee_id: int = Field(..., gt=0)
    assigned_to_employee_id: int | None = None


class BugCreate(BaseModel):
    title: str = Field(..., min_length=1)
    description: str = Field(..., min_length=1)
    priority: Literal["low", "medium", "high", "critical"]
    status: Literal["open", "in_progress", "resolved", "closed"] = "open"
    created_by_employee_id: int = Field(..., gt=0)
    assigned_to_employee_id: int | None = None


class BugUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1)
    description: str | None = Field(default=None, min_length=1)
    priority: Literal["low", "medium", "high", "critical"] | None = None
    status: Literal["open", "in_progress", "resolved", "closed"] | None = None
    created_by_employee_id: int | None = Field(default=None, gt=0)
    assigned_to_employee_id: int | None = Field(default=None, gt=0)


employees_db: dict[int, Employee] = {
    1: Employee(id=1, name="Alice", email="alice@example.com", role="manager", active=True),
    2: Employee(id=2, name="Bob", email="bob@example.com", role="developer", active=True),
    3: Employee(id=3, name="Carol", email="carol@example.com", role="tester", active=True),
}

bugs_db: dict[int, Bug] = {
    1: Bug(
        id=1,
        title="Login button not responding",
        description="Clicking login button does nothing on Chrome.",
        priority="high",
        status="open",
        created_by_employee_id=3,
        assigned_to_employee_id=2,
    ),
}

_next_employee_id = count(start=4)
_next_bug_id = count(start=2)


def get_next_employee_id() -> int:
    return next(_next_employee_id)


def get_next_bug_id() -> int:
    return next(_next_bug_id)
