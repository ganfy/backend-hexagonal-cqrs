from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from src.contexts.users.infrastructure.user_api import router as user_router
from src.core.exceptions.custom_exceptions import UserNotFoundException

app = FastAPI(title="Backend Hexagonal CQRS")


@app.exception_handler(UserNotFoundException)
async def user_not_found_exception_handler(
    request: Request, exc: UserNotFoundException
):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"message": str(exc)},
    )


@app.get("/")
async def root():
    return {"message": "Welcome to the Hexagonal CQRS Backend!"}


app.include_router(user_router, prefix="/users", tags=["users"])
