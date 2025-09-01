import asyncio
import json

import aio_pika

from src.contexts.users.application.create_user_use_case import CreateUserUseCase
from src.contexts.users.domain.create_user import CreateUser
from src.contexts.users.infrastructure.user_repository import UserRepository
from src.core.config.settings import settings
from src.core.database.database import AsyncSessionLocal


async def main():
    connection = await aio_pika.connect_robust(settings.RABBITMQ_URL)
    queue_name = "user_creation_queue"

    async with connection:
        channel = await connection.channel()
        await channel.set_qos(prefetch_count=1)  # Process one message at a time

        queue = await channel.declare_queue(queue_name, durable=True)

        print(" [*] Waiting for messages. To exit press CTRL+C")

        async for message in queue:
            async with message.process():
                try:
                    data = json.loads(message.body.decode())
                    command = CreateUser(**data)
                    print(f" [x] Received command to create user: {command.email}")

                    # Inject dependencies and execute use case
                    async with AsyncSessionLocal() as session:
                        try:
                            user_repository = UserRepository(session)
                            use_case = CreateUserUseCase(user_repository)
                            await use_case.execute(command)
                            await session.commit()
                            print(f" [v] User {command.email} created successfully.")
                        except Exception as e:
                            await session.rollback()
                            print(f" [!] Error processing message: {e}")
                            # Optional: requeue the message or log the error

                except Exception as e:
                    print(f" [!] Invalid message format: {e}")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Interrupted")
