from collections.abc import AsyncGenerator
from fastapi import Request
from aio_pika import Channel


async def get_rabbit_channel(request: Request) -> AsyncGenerator[Channel, None]:
    pool = request.app.state.rmq_channel_pool
    async with pool.acquire() as channel:
        yield channel
