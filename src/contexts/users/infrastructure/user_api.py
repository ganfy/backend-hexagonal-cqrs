import uuid

import aio_pika
from fastapi import APIRouter, Depends, status

from src.contexts.users.application.get_user_use_case import GetUserUseCase
from src.contexts.users.domain.create_user import CreateUser
from src.contexts.users.domain.read_user import ReadUser
from src.contexts.users.infrastructure.user_dependencies import get_user_query_use_case
from src.core.config.settings import settings

router = APIRouter()


@router.post("/", status_code=status.HTTP_202_ACCEPTED)
async def create_user(command: CreateUser):
    """
    Endpoint to accept the request for creating a user.
    Publishes the command to a RabbitMQ queue for asynchronous processing.
    """
    connection = await aio_pika.connect_robust(settings.RABBITMQ_URL)
    async with connection:
        channel = await connection.channel()
        # Ensure that the queue exists
        queue_name = "user_creation_queue"
        await channel.declare_queue(queue_name, durable=True)

        # Serialize the command and publish it
        message_body = command.model_dump_json().encode()
        await channel.default_exchange.publish(
            aio_pika.Message(body=message_body),
            routing_key=queue_name,
        )
    return {"message": "User creation request accepted."}


@router.get("/{user_id}", response_model=ReadUser)
async def get_user_by_id(
    user_id: uuid.UUID, use_case: GetUserUseCase = Depends(get_user_query_use_case)
):
    """
    Endpoint to retrieve a user by their ID.
    """
    return await use_case.execute(user_id)
