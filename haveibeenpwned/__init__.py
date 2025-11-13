"""
Have I Been Pwned API Python Client

A comprehensive Python library for the Have I Been Pwned API.
"""

__version__ = "1.0.0"

from .api import HIBP
from .models import Breach, Paste, Subscription, SubscribedDomain
from .exceptions import (
    HIBPError,
    AuthenticationError,
    BadRequestError,
    RateLimitError,
    NotFoundError,
    ForbiddenError,
    ServiceUnavailableError,
)

__all__ = [
    "HIBP",
    "Breach",
    "Paste",
    "Subscription",
    "SubscribedDomain",
    "HIBPError",
    "AuthenticationError",
    "BadRequestError",
    "RateLimitError",
    "NotFoundError",
    "ForbiddenError",
    "ServiceUnavailableError",
]
