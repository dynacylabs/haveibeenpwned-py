"""
Tests for breach API endpoints.
"""

import pytest
import responses as responses_lib

from haveibeenpwned.breach import BreachAPI
from haveibeenpwned.client import BaseClient
from haveibeenpwned.models import Breach, SubscribedDomain
from haveibeenpwned.exceptions import NotFoundError
from tests.conftest import TEST_ACCOUNT_EXISTS, TEST_ACCOUNT_NOT_FOUND, skip_if_no_api_key


@pytest.mark.unit
class TestBreachAPIMocked:
    """Test BreachAPI with mocked responses."""
    
    def test_get_breaches_for_account_truncated(self, sample_breach_truncated):
        """Test getting breaches for account (truncated)."""
        client = BaseClient(api_key="test-key")
        api = BreachAPI(client)
        
        with responses_lib.RequestsMock() as rsps:
            rsps.add(
                responses_lib.GET,
                "https://haveibeenpwned.com/api/v3/breachedaccount/test%40example.com",
                json=[sample_breach_truncated],
                status=200
            )
            
            breaches = api.get_breaches_for_account("test@example.com")
            assert len(breaches) == 1
            assert breaches[0].name == "Adobe"
    
    def test_get_breaches_for_account_full(self, sample_breach_data):
        """Test getting full breach data for account."""
        client = BaseClient(api_key="test-key")
        api = BreachAPI(client)
        
        with responses_lib.RequestsMock() as rsps:
            rsps.add(
                responses_lib.GET,
                "https://haveibeenpwned.com/api/v3/breachedaccount/test%40example.com",
                json=[sample_breach_data],
                status=200
            )
            
            breaches = api.get_breaches_for_account(
                "test@example.com",
                truncate_response=False
            )
            assert len(breaches) == 1
            assert breaches[0].name == "Adobe"
            assert breaches[0].pwn_count == 152445165
            assert len(breaches[0].data_classes) > 0
    
    def test_get_breaches_for_account_with_domain_filter(self, sample_breach_data):
        """Test getting breaches filtered by domain."""
        client = BaseClient(api_key="test-key")
        api = BreachAPI(client)
        
        with responses_lib.RequestsMock() as rsps:
            rsps.add(
                responses_lib.GET,
                "https://haveibeenpwned.com/api/v3/breachedaccount/test%40example.com",
                json=[sample_breach_data],
                status=200
            )
            
            breaches = api.get_breaches_for_account(
                "test@example.com",
                domain="adobe.com"
            )
            assert len(breaches) == 1
            
            # Check query params
            assert "domain=adobe.com" in rsps.calls[0].request.url
    
    def test_get_breaches_for_account_exclude_unverified(self, sample_breach_data):
        """Test excluding unverified breaches."""
        client = BaseClient(api_key="test-key")
        api = BreachAPI(client)
        
        with responses_lib.RequestsMock() as rsps:
            rsps.add(
                responses_lib.GET,
                "https://haveibeenpwned.com/api/v3/breachedaccount/test%40example.com",
                json=[sample_breach_data],
                status=200
            )
            
            breaches = api.get_breaches_for_account(
                "test@example.com",
                include_unverified=False
            )
            assert len(breaches) == 1
            
            # Check query params
            assert "includeUnverified=false" in rsps.calls[0].request.url
    
    def test_get_breaches_for_account_not_found(self):
        """Test account not found in breaches."""
        client = BaseClient(api_key="test-key")
        api = BreachAPI(client)
        
        with responses_lib.RequestsMock() as rsps:
            rsps.add(
                responses_lib.GET,
                "https://haveibeenpwned.com/api/v3/breachedaccount/notfound%40example.com",
                status=404
            )
            
            breaches = api.get_breaches_for_account("notfound@example.com")
            assert breaches == []
    
    def test_get_all_breaches(self, sample_breach_data):
        """Test getting all breaches."""
        client = BaseClient()
        api = BreachAPI(client)
        
        with responses_lib.RequestsMock() as rsps:
            rsps.add(
                responses_lib.GET,
                "https://haveibeenpwned.com/api/v3/breaches",
                json=[sample_breach_data, sample_breach_data],
                status=200
            )
            
            breaches = api.get_all_breaches()
            assert len(breaches) == 2
            assert all(isinstance(b, Breach) for b in breaches)
    
    def test_get_all_breaches_filtered_by_domain(self, sample_breach_data):
        """Test getting all breaches filtered by domain."""
        client = BaseClient()
        api = BreachAPI(client)
        
        with responses_lib.RequestsMock() as rsps:
            rsps.add(
                responses_lib.GET,
                "https://haveibeenpwned.com/api/v3/breaches",
                json=[sample_breach_data],
                status=200
            )
            
            breaches = api.get_all_breaches(domain="adobe.com")
            assert len(breaches) == 1
            assert "domain=adobe.com" in rsps.calls[0].request.url
    
    def test_get_all_breaches_spam_list_filter(self, sample_breach_data):
        """Test filtering spam list breaches."""
        client = BaseClient()
        api = BreachAPI(client)
        
        with responses_lib.RequestsMock() as rsps:
            rsps.add(
                responses_lib.GET,
                "https://haveibeenpwned.com/api/v3/breaches",
                json=[sample_breach_data],
                status=200
            )
            
            breaches = api.get_all_breaches(is_spam_list=True)
            assert "isSpamList=true" in rsps.calls[0].request.url
            
            breaches = api.get_all_breaches(is_spam_list=False)
            assert "isSpamList=false" in rsps.calls[-1].request.url
    
    def test_get_breach(self, sample_breach_data):
        """Test getting a single breach by name."""
        client = BaseClient()
        api = BreachAPI(client)
        
        with responses_lib.RequestsMock() as rsps:
            rsps.add(
                responses_lib.GET,
                "https://haveibeenpwned.com/api/v3/breach/Adobe",
                json=sample_breach_data,
                status=200
            )
            
            breach = api.get_breach("Adobe")
            assert breach.name == "Adobe"
            assert breach.pwn_count == 152445165
    
    def test_get_breach_not_found(self):
        """Test getting a breach that doesn't exist."""
        client = BaseClient()
        api = BreachAPI(client)
        
        with responses_lib.RequestsMock() as rsps:
            rsps.add(
                responses_lib.GET,
                "https://haveibeenpwned.com/api/v3/breach/NonExistent",
                status=404
            )
            
            with pytest.raises(NotFoundError):
                api.get_breach("NonExistent")
    
    def test_get_latest_breach(self, sample_breach_data):
        """Test getting the latest breach."""
        client = BaseClient()
        api = BreachAPI(client)
        
        with responses_lib.RequestsMock() as rsps:
            rsps.add(
                responses_lib.GET,
                "https://haveibeenpwned.com/api/v3/latestbreach",
                json=sample_breach_data,
                status=200
            )
            
            breach = api.get_latest_breach()
            assert breach.name == "Adobe"
    
    def test_get_data_classes(self, sample_data_classes):
        """Test getting all data classes."""
        client = BaseClient()
        api = BreachAPI(client)
        
        with responses_lib.RequestsMock() as rsps:
            rsps.add(
                responses_lib.GET,
                "https://haveibeenpwned.com/api/v3/dataclasses",
                json=sample_data_classes,
                status=200
            )
            
            data_classes = api.get_data_classes()
            assert len(data_classes) == 10
            assert "Email addresses" in data_classes[0] or "Account balances" in data_classes[0]
    
    def test_get_breached_domain(self):
        """Test getting breached domain."""
        client = BaseClient(api_key="test-key")
        api = BreachAPI(client)
        
        with responses_lib.RequestsMock() as rsps:
            rsps.add(
                responses_lib.GET,
                "https://haveibeenpwned.com/api/v3/breacheddomain/example.com",
                json={
                    "user1": ["Adobe"],
                    "user2": ["Adobe", "LinkedIn"]
                },
                status=200
            )
            
            result = api.get_breached_domain("example.com")
            assert "user1" in result
            assert "user2" in result
            assert len(result["user1"]) == 1
            assert len(result["user2"]) == 2
    
    def test_get_breached_domain_not_found(self):
        """Test getting breached domain that doesn't exist."""
        client = BaseClient(api_key="test-key")
        api = BreachAPI(client)
        
        with responses_lib.RequestsMock() as rsps:
            rsps.add(
                responses_lib.GET,
                "https://haveibeenpwned.com/api/v3/breacheddomain/example.com",
                status=404
            )
            
            result = api.get_breached_domain("example.com")
            assert result == {}
    
    def test_get_subscribed_domains(self, sample_subscribed_domain_data):
        """Test getting subscribed domains."""
        client = BaseClient(api_key="test-key")
        api = BreachAPI(client)
        
        with responses_lib.RequestsMock() as rsps:
            rsps.add(
                responses_lib.GET,
                "https://haveibeenpwned.com/api/v3/subscribeddomains",
                json=[sample_subscribed_domain_data],
                status=200
            )
            
            domains = api.get_subscribed_domains()
            assert len(domains) == 1
            assert isinstance(domains[0], SubscribedDomain)
            assert domains[0].domain_name == "example.com"


@pytest.mark.integration
@skip_if_no_api_key()
class TestBreachAPILive:
    """Test BreachAPI with live API (requires HIBP_API_KEY env var)."""
    
    def test_get_breaches_for_account_live(self, live_client):
        """Test getting breaches for test account."""
        breaches = live_client.breaches.get_breaches_for_account(TEST_ACCOUNT_EXISTS)
        assert isinstance(breaches, list)
        # Test account should have at least some breaches
        if breaches:
            assert all(isinstance(b, Breach) for b in breaches)
    
    def test_get_all_breaches_live(self, live_client):
        """Test getting all breaches."""
        breaches = live_client.breaches.get_all_breaches()
        assert isinstance(breaches, list)
        assert len(breaches) > 0
        assert all(isinstance(b, Breach) for b in breaches)
    
    def test_get_breach_live(self, live_client):
        """Test getting Adobe breach."""
        breach = live_client.breaches.get_breach("Adobe")
        assert breach.name == "Adobe"
        assert breach.domain == "adobe.com"
        assert breach.pwn_count > 0
    
    def test_get_data_classes_live(self, live_client):
        """Test getting data classes."""
        data_classes = live_client.breaches.get_data_classes()
        assert isinstance(data_classes, list)
        assert len(data_classes) > 0
        assert "Email addresses" in data_classes or "Passwords" in data_classes
