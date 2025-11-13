"""
Custom exceptions for the Have I Been Pwned API client.
"""


class HIBPError(Exception):
    """Base exception for HIBP API errors."""
    pass


class AuthenticationError(HIBPError):
    """Raised when API key authentication fails."""
    pass


class BadRequestError(HIBPError):
    """Raised when the request format is invalid."""
    pass


class RateLimitError(HIBPError):
    """Raised when the API rate limit is exceeded."""
    
    def __init__(self, message, retry_after=None):
        super().__init__(message)
        self.retry_after = retry_after


class NotFoundError(HIBPError):
    """Raised when the requested resource is not found."""
    pass


class ForbiddenError(HIBPError):
    """Raised when access is forbidden (e.g., missing user agent)."""
    pass


class ServiceUnavailableError(HIBPError):
    """Raised when the service is unavailable."""
    pass
