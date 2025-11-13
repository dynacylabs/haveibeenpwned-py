"""
Tests for the base client and exception handling.
"""

import pytest
import responses as responses_lib
from requests.exceptions import Timeout, RequestException

from haveibeenpwned.client import BaseClient
from haveibeenpwned.exceptions import (
    HIBPError,
    AuthenticationError,
    BadRequestError,
    RateLimitError,
    NotFoundError,
    ForbiddenError,
    ServiceUnavailableError,
)


@pytest.mark.unit
class TestBaseClient:
    """Test BaseClient class."""
    
    def test_initialization(self):
        """Test client initialization."""
        client = BaseClient(api_key="test-key", user_agent="test-agent", timeout=60)
        assert client.api_key == "test-key"
        assert client.user_agent == "test-agent"
        assert client.timeout == 60
    
    def test_initialization_defaults(self):
        """Test client initialization with defaults."""
        client = BaseClient()
        assert client.api_key is None
        assert client.user_agent == "haveibeenpwned-python-client"
        assert client.timeout == 30
    
    def test_get_headers_with_api_key(self):
        """Test header generation with API key."""
        client = BaseClient(api_key="test-key", user_agent="test-agent")
        headers = client._get_headers(include_api_key=True)
        assert headers["User-Agent"] == "test-agent"
        assert headers["hibp-api-key"] == "test-key"
    
    def test_get_headers_without_api_key(self):
        """Test header generation without API key."""
        client = BaseClient(api_key="test-key", user_agent="test-agent")
        headers = client._get_headers(include_api_key=False)
        assert headers["User-Agent"] == "test-agent"
        assert "hibp-api-key" not in headers
    
    def test_get_headers_no_api_key_available(self):
        """Test header generation when no API key is set."""
        client = BaseClient(user_agent="test-agent")
        headers = client._get_headers(include_api_key=True)
        assert "hibp-api-key" not in headers
    
    def test_url_encode(self):
        """Test URL encoding."""
        assert BaseClient.url_encode("test@example.com") == "test%40example.com"
        assert BaseClient.url_encode("test+user@example.com") == "test%2Buser%40example.com"
        assert BaseClient.url_encode("test user") == "test%20user"


@pytest.mark.unit
class TestClientErrorHandling:
    """Test client error handling with mocked responses."""
    
    @responses_lib.activate
    def test_200_response(self):
        """Test successful 200 response."""
        client = BaseClient()
        responses_lib.add(
            responses_lib.GET,
            "https://haveibeenpwned.com/api/v3/test",
            json={"result": "success"},
            status=200
        )
        
        result = client.get("test", include_api_key=False)
        assert result == {"result": "success"}
    
    @responses_lib.activate
    def test_200_empty_response(self):
        """Test 200 with empty response body."""
        client = BaseClient()
        responses_lib.add(
            responses_lib.GET,
            "https://haveibeenpwned.com/api/v3/test",
            body="",
            status=200
        )
        
        result = client.get("test", include_api_key=False)
        assert result is None
    
    @responses_lib.activate
    def test_400_bad_request(self):
        """Test 400 Bad Request error."""
        client = BaseClient()
        responses_lib.add(
            responses_lib.GET,
            "https://haveibeenpwned.com/api/v3/test",
            body="Invalid request format",
            status=400
        )
        
        with pytest.raises(BadRequestError) as exc_info:
            client.get("test", include_api_key=False)
        assert "Invalid request format" in str(exc_info.value)
    
    @responses_lib.activate
    def test_401_unauthorized(self):
        """Test 401 Unauthorized error."""
        client = BaseClient()
        responses_lib.add(
            responses_lib.GET,
            "https://haveibeenpwned.com/api/v3/test",
            body="Invalid API key",
            status=401
        )
        
        with pytest.raises(AuthenticationError) as exc_info:
            client.get("test", include_api_key=False)
        assert "Invalid API key" in str(exc_info.value)
    
    @responses_lib.activate
    def test_403_forbidden(self):
        """Test 403 Forbidden error."""
        client = BaseClient()
        responses_lib.add(
            responses_lib.GET,
            "https://haveibeenpwned.com/api/v3/test",
            body="Missing user agent",
            status=403
        )
        
        with pytest.raises(ForbiddenError) as exc_info:
            client.get("test", include_api_key=False)
        assert "Missing user agent" in str(exc_info.value)
    
    @responses_lib.activate
    def test_404_not_found(self):
        """Test 404 Not Found error."""
        client = BaseClient()
        responses_lib.add(
            responses_lib.GET,
            "https://haveibeenpwned.com/api/v3/test",
            status=404
        )
        
        with pytest.raises(NotFoundError):
            client.get("test", include_api_key=False)
    
    @responses_lib.activate
    def test_429_rate_limit(self):
        """Test 429 Rate Limit error."""
        client = BaseClient()
        responses_lib.add(
            responses_lib.GET,
            "https://haveibeenpwned.com/api/v3/test",
            body="Rate limit exceeded",
            status=429,
            headers={"retry-after": "5"}
        )
        
        with pytest.raises(RateLimitError) as exc_info:
            client.get("test", include_api_key=False)
        assert exc_info.value.retry_after == 5
        assert "Rate limit exceeded" in str(exc_info.value)
    
    @responses_lib.activate
    def test_429_rate_limit_no_retry_after(self):
        """Test 429 without retry-after header."""
        client = BaseClient()
        responses_lib.add(
            responses_lib.GET,
            "https://haveibeenpwned.com/api/v3/test",
            status=429
        )
        
        with pytest.raises(RateLimitError) as exc_info:
            client.get("test", include_api_key=False)
        assert exc_info.value.retry_after is None
    
    @responses_lib.activate
    def test_503_service_unavailable(self):
        """Test 503 Service Unavailable error."""
        client = BaseClient()
        responses_lib.add(
            responses_lib.GET,
            "https://haveibeenpwned.com/api/v3/test",
            body="Service temporarily unavailable",
            status=503
        )
        
        with pytest.raises(ServiceUnavailableError) as exc_info:
            client.get("test", include_api_key=False)
        assert "Service temporarily unavailable" in str(exc_info.value)
    
    @responses_lib.activate
    def test_500_unexpected_error(self):
        """Test unexpected 500 error."""
        client = BaseClient()
        responses_lib.add(
            responses_lib.GET,
            "https://haveibeenpwned.com/api/v3/test",
            body="Internal server error",
            status=500
        )
        
        with pytest.raises(HIBPError) as exc_info:
            client.get("test", include_api_key=False)
        assert "500" in str(exc_info.value)
    
    @responses_lib.activate
    def test_timeout_error(self):
        """Test timeout handling."""
        client = BaseClient(timeout=1)
        responses_lib.add(
            responses_lib.GET,
            "https://haveibeenpwned.com/api/v3/test",
            body=Timeout()
        )
        
        with pytest.raises(HIBPError) as exc_info:
            client.get("test", include_api_key=False)
        assert "timed out" in str(exc_info.value).lower()
    
    @responses_lib.activate
    def test_request_exception(self):
        """Test general request exception handling."""
        client = BaseClient()
        responses_lib.add(
            responses_lib.GET,
            "https://haveibeenpwned.com/api/v3/test",
            body=RequestException("Network error")
        )
        
        with pytest.raises(HIBPError) as exc_info:
            client.get("test", include_api_key=False)
        assert "Request failed" in str(exc_info.value)


@pytest.mark.unit
class TestClientRequests:
    """Test client request methods."""
    
    @responses_lib.activate
    def test_get_with_params(self):
        """Test GET request with query parameters."""
        client = BaseClient()
        responses_lib.add(
            responses_lib.GET,
            "https://haveibeenpwned.com/api/v3/test",
            json={"result": "success"},
            status=200
        )
        
        result = client.get("test", params={"foo": "bar", "baz": "qux"}, include_api_key=False)
        assert result == {"result": "success"}
        
        # Check that params were sent
        assert len(responses_lib.calls) == 1
        assert "foo=bar" in responses_lib.calls[0].request.url
        assert "baz=qux" in responses_lib.calls[0].request.url
    
    @responses_lib.activate
    def test_get_with_custom_base_url(self):
        """Test GET request with custom base URL."""
        client = BaseClient()
        responses_lib.add(
            responses_lib.GET,
            "https://api.pwnedpasswords.com/range/21BD1",
            body="test response",
            status=200
        )
        
        client.get("range/21BD1", base_url="https://api.pwnedpasswords.com", include_api_key=False)
        
        assert len(responses_lib.calls) == 1
        assert responses_lib.calls[0].request.url == "https://api.pwnedpasswords.com/range/21BD1"
