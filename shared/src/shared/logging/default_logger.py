import logging
from shared.logging import Logger


class DefaultLogger(Logger):
    def __init__(self, name: str = "App"):
        self._logger = logging.getLogger(name)

    def info(self, message: str) -> None:
        self._logger.info(message)

    def warning(self, message: str) -> None:
        self._logger.warning(message)

    def error(self, message: str, exc_info: bool = False) -> None:
        self._logger.error(message, exc_info)

    def debug(self, message: str) -> None:
        self._logger.debug(message)