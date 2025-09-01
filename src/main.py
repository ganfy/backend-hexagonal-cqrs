from fastapi import FastAPI

from src.contexts.users.infrastructure.user_api import router as user_router

app = FastAPI(title="Backend Hexagonal CQRS")


@app.get("/")
async def root():
    return {"message": "Welcome to the Hexagonal CQRS Backend!"}


app.include_router(user_router, prefix="/users", tags=["users"])
