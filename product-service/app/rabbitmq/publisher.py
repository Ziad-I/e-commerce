from aio_pika import Channel, Message

from app.core.config import settings


async def publish_message(channel: Channel, routing_key: str, message: str) -> None:
    """Publish a message to a RabbitMQ exchange."""
    exchange = await channel.declare_exchange(
        settings.RABBITMQ_EXCHANGE_NAME, durable=True
    )
    await exchange.publish(Message(body=message.encode()), routing_key=routing_key)
