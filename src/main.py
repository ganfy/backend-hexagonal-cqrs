from fastapi import FastAPI

app = FastAPI(title="Backend Hexagonal CQRS")


@app.get("/")
async def root():
    return {"message": "Welcome to the Hexagonal CQRS Backend!"}
