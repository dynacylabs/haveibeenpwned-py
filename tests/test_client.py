"""
Tests for the base client and exception handling.
"""

import pytest
import responses as responses_lib
from requests.exceptions import Timeout, RequestException

from hibp.client import BaseClient
from hibp.exceptions import (
    HIBPError,
    AuthenticationError,
    BadRequestError,
    RateLimitError,
    NotFoundError,
    ForbiddenError,
    ServiceUnavailableError,
)
from tests.conftest import requires_api_key


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
            json={"test": "response"},
            status=200
        )
        
        result = client.get("range/21BD1", base_url="https://api.pwnedpasswords.com", include_api_key=False)
        
        assert len(responses_lib.calls) == 1
        assert responses_lib.calls[0].request.url == "https://api.pwnedpasswords.com/range/21BD1"
        assert result == {"test": "response"}


@pytest.mark.integration
class TestBaseClientLive:
    """Live integration tests for BaseClient."""
    
    def test_live_request_without_api_key(self):
        """Test making a live request without API key (public endpoints)."""
        from tests.conftest import skip_if_no_api_key
        # This test doesn't actually need the skip, but keeping consistent
        client = BaseClient(user_agent="hibp-test-suite")
        
        # Test public endpoint - get all breaches
        breaches = client.get("breaches", include_api_key=False)
        
        assert breaches is not None
        assert isinstance(breaches, list)
        assert len(breaches) > 0
        assert "Name" in breaches[0]
    
    @requires_api_key
    def test_live_request_with_api_key(self):
        """Test making a live request with API key."""
        from tests.conftest import LIVE_API_KEY, TEST_ACCOUNT_EXISTS
        client = BaseClient(api_key=LIVE_API_KEY, user_agent="hibp-test-suite")
        
        # Test authenticated endpoint
        encoded_account = client.url_encode(TEST_ACCOUNT_EXISTS)
        breaches = client.get(f"breachedaccount/{encoded_account}")
        
        assert breaches is not None
        assert isinstance(breaches, list)
    
    def test_live_pwned_passwords_request(self):
        """Test live request to Pwned Passwords API."""
        client = BaseClient(user_agent="hibp-test-suite")
        
        # Test Pwned Passwords endpoint (no API key needed)
        response = client.session.get(
            f"{client.PWNED_PASSWORDS_URL}/range/21BD1",
            headers=client._get_headers(include_api_key=False),
            timeout=client.timeout
        )
        
        assert response.status_code == 200
        assert len(response.text) > 0
        assert ":" in response.text  # Hash:count format
    
    @requires_api_key
    def test_live_headers_sent(self):
        """Test that correct headers are sent in live requests."""
        from tests.conftest import LIVE_API_KEY
        client = BaseClient(api_key=LIVE_API_KEY, user_agent="hibp-live-test")
        
        # Make a request and verify headers would be sent
        headers = client._get_headers(include_api_key=True)
        
        assert headers["User-Agent"] == "hibp-live-test"
        assert "hibp-api-key" in headers
        assert headers["hibp-api-key"] == LIVE_API_KEY
    
    def test_live_url_encoding(self):
        """Test URL encoding with live requests."""
        client = BaseClient(user_agent="hibp-test-suite")
        
        # Test encoding special characters
        encoded = client.url_encode("test+user@example.com")
        assert "+" not in encoded or encoded.count("+") == 0 or "%2B" in encoded
        
        encoded = client.url_encode("test@example.com")
        assert "@" not in encoded or "%40" in encoded
    
    def test_live_not_found_handling(self):
        """Test handling of 404 responses in live requests."""
        from hibp.exceptions import NotFoundError
        client = BaseClient(user_agent="hibp-test-suite")
        
        # Try to get a breach that doesn't exist
        with pytest.raises(NotFoundError):
            client.get("breach/ThisBreachDefinitelyDoesNotExist123456", include_api_key=False)
    
    @requires_api_key
    def test_live_authentication_with_invalid_key(self):
        """Test authentication failure with invalid API key."""
        from hibp.exceptions import AuthenticationError
        from tests.conftest import TEST_ACCOUNT_EXISTS
        
        client = BaseClient(api_key="invalid-key-12345678901234567890", user_agent="hibp-test-suite")
        encoded_account = client.url_encode(TEST_ACCOUNT_EXISTS)
        
        # Should raise authentication error
        with pytest.raises(AuthenticationError):
            client.get(f"breachedaccount/{encoded_account}")
