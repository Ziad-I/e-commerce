import json
from loguru import logger
from functools import lru_cache
from aio_pika import IncomingMessage, connect_robust, ExchangeType, Message, Queue

from app.core.config import settings
from app.elastic.elastic import get_elastic_client


class RabbitMQConsumer:
    def __init__(self, url: str, exchange_name: str):
        self.url = url
        self.exchange_name = exchange_name
        self.connection = None
        self.channel = None

    async def connect(self):
        """Establish a connection to RabbitMQ."""
        self.connection = await connect_robust(self.url)
        self.channel = await self.connection.channel()
        self.exchange = await self.channel.declare_exchange(
            self.exchange_name,
            ExchangeType.TOPIC,
            durable=True,
        )
        self.queue = await self.channel.declare_queue("", exclusive=True)
        await self.queue.bind(self.exchange, routing_key="product.*")
        await self.queue.consume(self.on_message)

    async def close(self):
        """Close the RabbitMQ connection."""
        if self.connection:
            await self.connection.close()
            self.connection = None
            self.channel = None
            self.exchange = None
            self.queue = None

    async def on_message(self, message: IncomingMessage):
        """Callback for processing incoming messages."""
        # Ensure the message is processed correctly
        es = get_elastic_client()
        async with message.process():
            product = json.loads(message.body.decode())
            routing_key = message.routing_key
            op = routing_key.split(".")[-1]
            if op == "create":
                resp = await es.index_product(
                    index=settings.ELASTICSEARCH_INDEX,
                    id=product["id"],
                    document=product,
                )
            elif op == "update":
                resp = await es.update_product(
                    index=settings.ELASTICSEARCH_INDEX,
                    id=product["id"],
                    document=product,
                )
            elif op == "delete":
                resp = await es.delete_product(
                    index=settings.ELASTICSEARCH_INDEX,
                    id=product["id"],
                )
            else:
                message.reject()
                logger.error(f"Unknown operation: {op}")


@lru_cache
def get_rabbitmq_client() -> RabbitMQConsumer:
    """Get a singleton instance of RabbitMQConsumer."""
    return RabbitMQConsumer(
        url=settings.rabbitmq_url,
        exchange_name=settings.RABBITMQ_EXCHANGE_NAME,
    )
