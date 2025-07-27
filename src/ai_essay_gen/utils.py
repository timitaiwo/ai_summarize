import logging
from dataclasses import dataclass


@dataclass
class AuthorEssayKV:
    """ """

    author_profile: str
    author_essay: str


class AIRequestError(Exception):
    """
    Error with AI request
    """

    pass


def create_logger(name: str):
    """ """
    # Configure logging
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger
