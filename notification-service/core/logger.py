import logging
import sys
from typing import Any, Union

from loguru import logger

from core.config import settings


class InterceptHandler(logging.Handler):
    """
    Default handler from examples in loguru documentation.

    This handler intercepts all log requests and
    passes them to loguru.

    For more info see:
    https://loguru.readthedocs.io/en/stable/overview.html#entirely-compatible-with-standard-logging
    """

    def emit(self, record: logging.LogRecord) -> None:
        """
        Propagates logs to loguru.

        :param record: record to log.
        """
        try:
            level: Union[str, int] = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # Find caller from where originated the logged message
        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(
            level,
            record.getMessage(),
        )


def configure_logging() -> None:
    """Configures logging."""
    intercept_handler = InterceptHandler()

    logging.basicConfig(handlers=[intercept_handler], level=logging.NOTSET)

    for name in logging.root.manager.loggerDict.keys():
        logging.getLogger(name).handlers = []
        logging.getLogger(name).propagate = True

    # set logs output, level and format
    logger.remove()
    logger.add(
        sys.stderr,
        colorize=True,
        level=settings.LOG_LEVEL.value,
    )
