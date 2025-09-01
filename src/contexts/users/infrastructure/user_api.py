import aio_pika
from fastapi import APIRouter, status

from src.contexts.users.domain.create_user import CreateUser
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
