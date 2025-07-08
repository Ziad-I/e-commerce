import asyncio
import grpc
from fastapi import FastAPI
from contextlib import suppress
from loguru import logger

from app.core.config import settings
from app.proto import price_pb2, price_pb2_grpc
from app.crud import product as product_crud


class PriceService(price_pb2_grpc.PriceServiceServicer):
    async def GetPrice(self, request, context):
        """
        Handle the GetPrice request and return a response.
        """
        product = await product_crud.get_product_by_id(request.product_id)
        if not product:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details(f"Product with ID {request.product_id} not found.")
            return price_pb2.PriceResponse()

        price = product.price
        return price_pb2.PriceResponse(price=price)


async def serve_grpc():
    server = grpc.aio.server()
    price_pb2_grpc.add_PriceServiceServicer_to_server(PriceService(), server)
    port = settings.PRICE_SERVICE_GRPC_PORT
    host = settings.PRICE_SERVICE_GRPC_HOST
    server.add_insecure_port(f"{host}:{port}")
    logger.info(f"Starting Price Service gRPC server on {host}:{port}")
    await server.start()
    await server.wait_for_termination()


async def init_price_service(app: FastAPI):
    """
    Initialize the Price Service gRPC server.
    """
    app.state.grpc_server = asyncio.create_task(serve_grpc())


async def close_price_service(app: FastAPI):
    """
    Close the Price Service gRPC server.
    """
    if hasattr(app.state, "grpc_server"):
        app.state.grpc_server.cancel()
        with suppress(asyncio.CancelledError):
            await app.state.grpc_server
