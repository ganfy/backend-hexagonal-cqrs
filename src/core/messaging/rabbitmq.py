import aio_pika

from src.core.config.settings import settings


async def get_rabbitmq_channel():
    connection = await aio_pika.connect_robust(settings.RABBITMQ_URL)
    channel = await connection.channel()
    try:
        yield channel
    finally:
        await channel.close()
        await connection.close()
