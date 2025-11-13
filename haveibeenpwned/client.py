"""
Base client for making HTTP requests to the Have I Been Pwned API.
"""

import time
from typing import Optional, Dict, Any
from urllib.parse import quote

import requests

from .exceptions import (
    AuthenticationError,
    BadRequestError,
    RateLimitError,
    NotFoundError,
    ForbiddenError,
    ServiceUnavailableError,
    HIBPError,
)


class BaseClient:
    """Base HTTP client for the HIBP API."""
    
    BASE_URL = "https://haveibeenpwned.com/api/v3"
    PWNED_PASSWORDS_URL = "https://api.pwnedpasswords.com"
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        user_agent: str = "haveibeenpwned-python-client",
        timeout: int = 30,
    ):
        """
        Initialize the base client.
        
        Args:
            api_key: HIBP API key for authenticated endpoints
            user_agent: User agent string for API requests
            timeout: Request timeout in seconds
        """
        self.api_key = api_key
        self.user_agent = user_agent
        self.timeout = timeout
        self.session = requests.Session()
        
    def _get_headers(self, include_api_key: bool = True) -> Dict[str, str]:
        """
        Get headers for API requests.
        
        Args:
            include_api_key: Whether to include the API key in headers
            
        Returns:
            Dictionary of headers
        """
        headers = {
            "User-Agent": self.user_agent,
        }
        
        if include_api_key and self.api_key:
            headers["hibp-api-key"] = self.api_key
            
        return headers
    
    def _handle_response(self, response: requests.Response) -> Any:
        """
        Handle API response and raise appropriate exceptions.
        
        Args:
            response: Response object from requests
            
        Returns:
            Parsed JSON response or None for 404
            
        Raises:
            Various HIBP exceptions based on status code
        """
        if response.status_code == 200:
            # Handle empty responses
            if not response.content:
                return None
            return response.json()
        
        elif response.status_code == 400:
            raise BadRequestError(
                f"Bad request: {response.text or 'Invalid request format'}"
            )
        
        elif response.status_code == 401:
            raise AuthenticationError(
                f"Unauthorized: {response.text or 'Invalid API key'}"
            )
        
        elif response.status_code == 403:
            raise ForbiddenError(
                f"Forbidden: {response.text or 'Missing or invalid user agent'}"
            )
        
        elif response.status_code == 404:
            raise NotFoundError("Resource not found")
        
        elif response.status_code == 429:
            retry_after = response.headers.get("retry-after")
            retry_after_int = int(retry_after) if retry_after else None
            raise RateLimitError(
                f"Rate limit exceeded. Retry after {retry_after} seconds.",
                retry_after=retry_after_int,
            )
        
        elif response.status_code == 503:
            raise ServiceUnavailableError(
                f"Service unavailable: {response.text or 'Try again later'}"
            )
        
        else:
            raise HIBPError(
                f"Unexpected status code {response.status_code}: {response.text}"
            )
    
    def get(
        self,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        include_api_key: bool = True,
        base_url: Optional[str] = None,
    ) -> Any:
        """
        Make a GET request to the API.
        
        Args:
            endpoint: API endpoint path
            params: Query parameters
            include_api_key: Whether to include API key in headers
            base_url: Override the base URL (for Pwned Passwords API)
            
        Returns:
            Parsed JSON response or None for 404
        """
        url = f"{base_url or self.BASE_URL}/{endpoint}"
        headers = self._get_headers(include_api_key=include_api_key)
        
        try:
            response = self.session.get(
                url,
                headers=headers,
                params=params,
                timeout=self.timeout,
            )
            return self._handle_response(response)
        except requests.exceptions.Timeout:
            raise HIBPError(f"Request timed out after {self.timeout} seconds")
        except requests.exceptions.RequestException as e:
            raise HIBPError(f"Request failed: {str(e)}")
    
    @staticmethod
    def url_encode(value: str) -> str:
        """
        URL encode a value for use in API requests.
        
        Args:
            value: String to encode
            
        Returns:
            URL-encoded string
        """
        return quote(value, safe="")
