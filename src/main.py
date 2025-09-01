from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from src.contexts.auth.infrastructure.auth_api import router as auth_router
from src.contexts.users.infrastructure.user_api import router as user_router
from src.core.exceptions.custom_exceptions import (
    InvalidCredentialsException,
    UserNotFoundException,
)

app = FastAPI(title="Backend Hexagonal CQRS")


@app.exception_handler(UserNotFoundException)
async def user_not_found_exception_handler(
    request: Request, exc: UserNotFoundException
):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"message": str(exc)},
    )


@app.exception_handler(InvalidCredentialsException)
async def invalid_credentials_exception_handler(
    request: Request, exc: InvalidCredentialsException
):
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={"message": str(exc)},
        headers={"WWW-Authenticate": "Bearer"},
    )


@app.get("/")
async def root():
    return {"message": "Welcome to the Hexagonal CQRS Backend!"}


app.include_router(user_router, prefix="/users", tags=["users"])
app.include_router(auth_router, prefix="/auth", tags=["auth"])
