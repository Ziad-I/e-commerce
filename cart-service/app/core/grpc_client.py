import grpc
from loguru import logger
from functools import lru_cache

from app.core.config import settings
from app.proto import price_pb2, price_pb2_grpc


class GrpcClient:
    def __init__(self):
        self._channel = grpc.aio.insecure_channel(
            f"{settings.PRICE_SERVICE_GRPC_HOST}:{settings.PRICE_SERVICE_GRPC_PORT}"
        )
        self._price_stub = price_pb2_grpc.PriceServiceStub(self._channel)
        logger.info("Connected to GRPC price service.")

    async def get_price(self, product_id: str) -> float:
        """
        Fetch the price of a product by its ID using gRPC.

        Args:
            product_id (str): The ID of the product.

        Returns:
            float: The price of the product.
        """
        try:
            response = await self._price_stub.GetPrice(
                price_pb2.GetPriceRequest(product_id=product_id)
            )
            return response.price
        except grpc.aio.AioRpcError as e:
            logger.error(
                f"gRPC error while fetching price for product {product_id}: {e.details()}"
            )
            return None

    async def close(self):
        """Close the GRPC channel."""
        await self._channel.close()


@lru_cache()
def get_grpc_client() -> GrpcClient:
    """Get a singleton instance of the GRPC client."""
    return GrpcClient()
