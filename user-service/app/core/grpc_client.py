import grpc
from loguru import logger
from functools import lru_cache

from app.core.config import settings
from app.proto import notification_pb2_grpc, notification_pb2


class GrpcClient:
    """GRPC client for interacting with the notification service."""

    def __init__(self):
        self._channel = grpc.aio.insecure_channel(
            f"{settings.GRPC_HOST}:{settings.GRPC_PORT}"
        )
        self._notification_stub = notification_pb2_grpc.NotificationServiceStub(
            self._channel
        )

    async def send_email(self, email_request: notification_pb2.SendEmailRequest):
        """Send an email using the notification service."""
        try:
            response = await self._notification_stub.SendEmail(email_request)
            if response.success:
                logger.info(f"Email sent successfully to {email_request.to}.")
            else:
                logger.error(f"Failed to send email: {response.error}")
            return response
        except grpc.RpcError as e:
            logger.error(f"GRPC error: {e.code()} - {e.details()}")
            return notification_pb2.SendEmailResponse(success=False, error=str(e))
        except Exception as e:
            logger.error(f"Unexpected error while sending email: {e}")
            return notification_pb2.SendEmailResponse(success=False, error=str(e))

    async def close(self):
        """Close the GRPC channel."""
        await self._channel.close()


@lru_cache()
def get_grpc_client() -> GrpcClient:
    """Get a singleton instance of the GRPC client."""
    return GrpcClient()
