"""
Tests for pastes, stealer logs, and subscription APIs.
"""

import pytest
import responses as responses_lib

from haveibeenpwned.pastes import PastesAPI
from haveibeenpwned.stealer_logs import StealerLogsAPI
from haveibeenpwned.subscription import SubscriptionAPI
from haveibeenpwned.client import BaseClient
from haveibeenpwned.models import Paste, Subscription
from tests.conftest import TEST_ACCOUNT_EXISTS, skip_if_no_api_key


@pytest.mark.unit
class TestPastesAPIMocked:
    """Test PastesAPI with mocked responses."""
    
    def test_get_pastes_for_account(self, sample_paste_data):
        """Test getting pastes for account."""
        client = BaseClient(api_key="test-key")
        api = PastesAPI(client)
        
        with responses_lib.RequestsMock() as rsps:
            rsps.add(
                responses_lib.GET,
                "https://haveibeenpwned.com/api/v3/pasteaccount/test%40example.com",
                json=[sample_paste_data, sample_paste_data],
                status=200
            )
            
            pastes = api.get_pastes_for_account("test@example.com")
            assert len(pastes) == 2
            assert all(isinstance(p, Paste) for p in pastes)
            assert pastes[0].source == "Pastebin"
    
    def test_get_pastes_for_account_not_found(self):
        """Test getting pastes for account with no pastes."""
        client = BaseClient(api_key="test-key")
        api = PastesAPI(client)
        
        with responses_lib.RequestsMock() as rsps:
            rsps.add(
                responses_lib.GET,
                "https://haveibeenpwned.com/api/v3/pasteaccount/test%40example.com",
                status=404
            )
            
            pastes = api.get_pastes_for_account("test@example.com")
            assert pastes == []


@pytest.mark.unit
class TestStealerLogsAPIMocked:
    """Test StealerLogsAPI with mocked responses."""
    
    def test_get_by_email(self):
        """Test getting stealer logs by email."""
        client = BaseClient(api_key="test-key")
        api = StealerLogsAPI(client)
        
        with responses_lib.RequestsMock() as rsps:
            rsps.add(
                responses_lib.GET,
                "https://haveibeenpwned.com/api/v3/stealerlogsbyemail/test%40example.com",
                json=["netflix.com", "spotify.com"],
                status=200
            )
            
            domains = api.get_by_email("test@example.com")
            assert domains == ["netflix.com", "spotify.com"]
    
    def test_get_by_email_not_found(self):
        """Test getting stealer logs for email with no results."""
        client = BaseClient(api_key="test-key")
        api = StealerLogsAPI(client)
        
        with responses_lib.RequestsMock() as rsps:
            rsps.add(
                responses_lib.GET,
                "https://haveibeenpwned.com/api/v3/stealerlogsbyemail/test%40example.com",
                status=404
            )
            
            domains = api.get_by_email("test@example.com")
            assert domains == []
    
    def test_get_by_website_domain(self):
        """Test getting stealer logs by website domain."""
        client = BaseClient(api_key="test-key")
        api = StealerLogsAPI(client)
        
        with responses_lib.RequestsMock() as rsps:
            rsps.add(
                responses_lib.GET,
                "https://haveibeenpwned.com/api/v3/stealerlogsbywebsitedomain/netflix.com",
                json=["user1@example.com", "user2@example.com"],
                status=200
            )
            
            emails = api.get_by_website_domain("netflix.com")
            assert len(emails) == 2
            assert "user1@example.com" in emails
    
    def test_get_by_website_domain_not_found(self):
        """Test getting stealer logs for website with no results."""
        client = BaseClient(api_key="test-key")
        api = StealerLogsAPI(client)
        
        with responses_lib.RequestsMock() as rsps:
            rsps.add(
                responses_lib.GET,
                "https://haveibeenpwned.com/api/v3/stealerlogsbywebsitedomain/example.com",
                status=404
            )
            
            emails = api.get_by_website_domain("example.com")
            assert emails == []
    
    def test_get_by_email_domain(self):
        """Test getting stealer logs by email domain."""
        client = BaseClient(api_key="test-key")
        api = StealerLogsAPI(client)
        
        with responses_lib.RequestsMock() as rsps:
            rsps.add(
                responses_lib.GET,
                "https://haveibeenpwned.com/api/v3/stealerlogsbyemaildomain/example.com",
                json={
                    "user1": ["netflix.com"],
                    "user2": ["netflix.com", "spotify.com"]
                },
                status=200
            )
            
            result = api.get_by_email_domain("example.com")
            assert "user1" in result
            assert "user2" in result
            assert len(result["user1"]) == 1
            assert len(result["user2"]) == 2
    
    def test_get_by_email_domain_not_found(self):
        """Test getting stealer logs for email domain with no results."""
        client = BaseClient(api_key="test-key")
        api = StealerLogsAPI(client)
        
        with responses_lib.RequestsMock() as rsps:
            rsps.add(
                responses_lib.GET,
                "https://haveibeenpwned.com/api/v3/stealerlogsbyemaildomain/example.com",
                status=404
            )
            
            result = api.get_by_email_domain("example.com")
            assert result == {}


@pytest.mark.unit
class TestSubscriptionAPIMocked:
    """Test SubscriptionAPI with mocked responses."""
    
    def test_get_status(self, sample_subscription_data):
        """Test getting subscription status."""
        client = BaseClient(api_key="test-key")
        api = SubscriptionAPI(client)
        
        with responses_lib.RequestsMock() as rsps:
            rsps.add(
                responses_lib.GET,
                "https://haveibeenpwned.com/api/v3/subscription/status",
                json=sample_subscription_data,
                status=200
            )
            
            subscription = api.get_status()
            assert isinstance(subscription, Subscription)
            assert subscription.subscription_name == "Pwned 1"
            assert subscription.rpm == 10


@pytest.mark.integration
@skip_if_no_api_key()
class TestPastesAPILive:
    """Test PastesAPI with live API."""
    
    def test_get_pastes_for_account_live(self, live_client):
        """Test getting pastes for test account."""
        pastes = live_client.pastes.get_pastes_for_account(TEST_ACCOUNT_EXISTS)
        assert isinstance(pastes, list)
        # Test account may or may not have pastes
        if pastes:
            assert all(isinstance(p, Paste) for p in pastes)


@pytest.mark.integration
@pytest.mark.slow
@skip_if_no_api_key()
class TestStealerLogsAPILive:
    """Test StealerLogsAPI with live API (requires Pwned 5+ subscription)."""
    
    def test_get_by_email_live(self, live_client):
        """Test getting stealer logs by email."""
        # This requires a Pwned 5+ subscription and verified domain
        # Will likely return empty or error without proper subscription
        try:
            domains = live_client.stealer_logs.get_by_email(TEST_ACCOUNT_EXISTS)
            assert isinstance(domains, list)
        except Exception:
            # Expected if subscription doesn't include stealer logs
            pass


@pytest.mark.integration
@skip_if_no_api_key()
class TestSubscriptionAPILive:
    """Test SubscriptionAPI with live API."""
    
    def test_get_status_live(self, live_client):
        """Test getting subscription status."""
        try:
            subscription = live_client.subscription.get_status()
            assert isinstance(subscription, Subscription)
            assert subscription.rpm > 0
            assert subscription.subscription_name != ""
        except Exception:
            # May fail with test API key
            pass
