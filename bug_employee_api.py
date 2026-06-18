from fastapi import FastAPI

from bug_api import router as bug_router
from employee_api import router as employee_router

app = FastAPI(title="Bug And Employee Management API")

app.include_router(employee_router)
app.include_router(bug_router)


@app.get("/")
def root() -> dict[str, str]:
    return {"message": "Bug And Employee Management API is running"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8001)
