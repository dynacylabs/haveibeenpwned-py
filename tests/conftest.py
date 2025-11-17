"""
Test configuration and fixtures.
"""

import os
import pytest
import responses as responses_lib
from typing import Dict, Any

from haveibeenpwned import HIBP


# Test API key (use real one for integration tests via env var)
TEST_API_KEY = "00000000000000000000000000000000"
LIVE_API_KEY = os.environ.get("HIBP_API_KEY", TEST_API_KEY) or TEST_API_KEY

# Test account emails
TEST_ACCOUNT_EXISTS = "account-exists@hibp-integration-tests.com"
TEST_ACCOUNT_SPAM = "spam-list-only@hibp-integration-tests.com"
TEST_ACCOUNT_STEALER = "stealer-log@hibp-integration-tests.com"
TEST_ACCOUNT_NOT_FOUND = "notfound@example.com"


@pytest.fixture
def mock_client():
    """Create a HIBP client with test API key."""
    return HIBP(api_key=TEST_API_KEY, user_agent="hibp-test-suite")


@pytest.fixture
def live_client():
    """Create a HIBP client for live API tests."""
    return HIBP(api_key=LIVE_API_KEY, user_agent="hibp-test-suite")


@pytest.fixture
def password_client():
    """Create a HIBP client without API key for password tests."""
    return HIBP(user_agent="hibp-test-suite")


@pytest.fixture
def responses():
    """Enable responses mock for HTTP requests."""
    with responses_lib.RequestsMock() as rsps:
        yield rsps


# Sample breach data
@pytest.fixture
def sample_breach_data() -> Dict[str, Any]:
    """Sample breach data for testing."""
    return {
        "Name": "Adobe",
        "Title": "Adobe",
        "Domain": "adobe.com",
        "BreachDate": "2013-10-04",
        "AddedDate": "2013-12-04T00:00:00Z",
        "ModifiedDate": "2022-05-15T23:52:49Z",
        "PwnCount": 152445165,
        "Description": "In October 2013, 153 million Adobe accounts were breached...",
        "LogoPath": "Adobe.png",
        "DataClasses": [
            "Email addresses",
            "Password hints",
            "Passwords",
            "Usernames"
        ],
        "IsVerified": True,
        "IsFabricated": False,
        "IsSensitive": False,
        "IsRetired": False,
        "IsSpamList": False,
        "IsMalware": False,
        "IsStealerLog": False,
        "IsSubscriptionFree": False,
        "Attribution": None
    }


@pytest.fixture
def sample_breach_truncated() -> Dict[str, Any]:
    """Sample truncated breach data."""
    return {"Name": "Adobe"}


@pytest.fixture
def sample_paste_data() -> Dict[str, Any]:
    """Sample paste data for testing."""
    return {
        "Source": "Pastebin",
        "Id": "8Q0BvKD8",
        "Title": "syslog",
        "Date": "2014-03-04T19:14:54Z",
        "EmailCount": 139
    }


@pytest.fixture
def sample_subscription_data() -> Dict[str, Any]:
    """Sample subscription data for testing."""
    return {
        "SubscriptionName": "Pwned 1",
        "Description": "Up to 10 passwords per minute",
        "SubscribedUntil": "2024-12-31T23:59:59Z",
        "Rpm": 10,
        "DomainSearchMaxBreachedAccounts": 100,
        "IncludesStealerLogs": False
    }


@pytest.fixture
def sample_subscribed_domain_data() -> Dict[str, Any]:
    """Sample subscribed domain data for testing."""
    return {
        "DomainName": "example.com",
        "PwnCount": 150,
        "PwnCountExcludingSpamLists": 120,
        "PwnCountExcludingSpamListsAtLastSubscriptionRenewal": 100,
        "NextSubscriptionRenewal": "2024-12-31T23:59:59Z"
    }


@pytest.fixture
def sample_data_classes() -> list:
    """Sample data classes."""
    return [
        "Account balances",
        "Age groups",
        "Ages",
        "Apps installed on devices",
        "Audio recordings",
        "Auth tokens",
        "Avatars",
        "Bank account numbers",
        "Banking PINs",
        "Beauty ratings",
    ]


@pytest.fixture
def sample_password_hash_response() -> str:
    """Sample Pwned Passwords API response."""
    return """0018A45C4D1DEF81644B54AB7F969B88D65:1
00D4F6E8FA6EECAD2A3AA415EEC418D38EC:2
011053FD0102E94D6AE2F8B83D76FAF94F6:1
012A7CA357541F0AC487871FEEC1891C49C:2
0136E006E24E7D152139815FB0FC6A50B15:2"""


def skip_if_no_api_key(client_fixture_name="live_client"):
    """Skip test if no live API key is available."""
    return pytest.mark.skipif(
        LIVE_API_KEY == TEST_API_KEY,
        reason="No live API key provided (set HIBP_API_KEY environment variable)"
    )


# Create a reusable skip marker
requires_api_key = pytest.mark.skipif(
    LIVE_API_KEY == TEST_API_KEY,
    reason="No live API key provided (set HIBP_API_KEY environment variable)"
)
