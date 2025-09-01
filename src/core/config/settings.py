from decouple import config


class Settings:
    APP_NAME: str = "Backend Hexagonal CQRS"
    DATABASE_URL: str = config(
        "DATABASE_URL",
        default="postgresql+asyncpg://user:password@localhost:5432/cqrs_project_database",
    )
    RABBITMQ_URL: str = config(
        "RABBITMQ_URL", default="amqp://guest:guest@localhost:5672/"
    )


settings = Settings()
