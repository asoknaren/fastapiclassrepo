from typing import Any

from fastapi import Body, FastAPI, HTTPException, Response, status

app = FastAPI(title="My calculator API", version="1.0.0")


@app.post("/add", status_code=status.HTTP_200_OK)
def add_numbers(a: int = Body(...), b: int = Body(...)) -> dict[str, Any]:
    return {"result": a + b}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8003)