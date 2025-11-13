"""
Tests for the main HIBP API interface.
"""

import pytest
import responses as responses_lib

from haveibeenpwned import HIBP
from haveibeenpwned.models import Breach, Paste, Subscription, SubscribedDomain
from tests.conftest import TEST_ACCOUNT_EXISTS, skip_if_no_api_key


@pytest.mark.unit
class TestHIBPInitialization:
    """Test HIBP class initialization."""
    
    def test_init_with_api_key(self):
        """Test initialization with API key."""
        hibp = HIBP(api_key="test-key")
        assert hibp.client.api_key == "test-key"
        assert hibp.breaches is not None
        assert hibp.passwords is not None
        assert hibp.pastes is not None
        assert hibp.stealer_logs is not None
        assert hibp.subscription is not None
    
    def test_init_without_api_key(self):
        """Test initialization without API key."""
        hibp = HIBP()
        assert hibp.client.api_key is None
        assert hibp.passwords is not None
    
    def test_init_custom_user_agent(self):
        """Test initialization with custom user agent."""
        hibp = HIBP(user_agent="custom-agent")
        assert hibp.client.user_agent == "custom-agent"
    
    def test_init_custom_timeout(self):
        """Test initialization with custom timeout."""
        hibp = HIBP(timeout=60)
        assert hibp.client.timeout == 60


@pytest.mark.unit
class TestHIBPConvenienceMethods:
    """Test HIBP convenience methods with mocked responses."""
    
    def test_get_account_breaches(self, sample_breach_data):
        """Test get_account_breaches convenience method."""
        hibp = HIBP(api_key="test-key")
        
        with responses_lib.RequestsMock() as rsps:
            rsps.add(
                responses_lib.GET,
                "https://haveibeenpwned.com/api/v3/breachedaccount/test%40example.com",
                json=[sample_breach_data],
                status=200
            )
            
            breaches = hibp.get_account_breaches("test@example.com")
            assert len(breaches) == 1
            assert isinstance(breaches[0], Breach)
    
    def test_get_all_breaches(self, sample_breach_data):
        """Test get_all_breaches convenience method."""
        hibp = HIBP()
        
        with responses_lib.RequestsMock() as rsps:
            rsps.add(
                responses_lib.GET,
                "https://haveibeenpwned.com/api/v3/breaches",
                json=[sample_breach_data],
                status=200
            )
            
            breaches = hibp.get_all_breaches()
            assert len(breaches) == 1
    
    def test_get_breach(self, sample_breach_data):
        """Test get_breach convenience method."""
        hibp = HIBP()
        
        with responses_lib.RequestsMock() as rsps:
            rsps.add(
                responses_lib.GET,
                "https://haveibeenpwned.com/api/v3/breach/Adobe",
                json=sample_breach_data,
                status=200
            )
            
            breach = hibp.get_breach("Adobe")
            assert breach.name == "Adobe"
    
    def test_get_latest_breach(self, sample_breach_data):
        """Test get_latest_breach convenience method."""
        hibp = HIBP()
        
        with responses_lib.RequestsMock() as rsps:
            rsps.add(
                responses_lib.GET,
                "https://haveibeenpwned.com/api/v3/latestbreach",
                json=sample_breach_data,
                status=200
            )
            
            breach = hibp.get_latest_breach()
            assert breach.name == "Adobe"
    
    def test_get_data_classes(self, sample_data_classes):
        """Test get_data_classes convenience method."""
        hibp = HIBP()
        
        with responses_lib.RequestsMock() as rsps:
            rsps.add(
                responses_lib.GET,
                "https://haveibeenpwned.com/api/v3/dataclasses",
                json=sample_data_classes,
                status=200
            )
            
            data_classes = hibp.get_data_classes()
            assert len(data_classes) > 0
    
    def test_get_domain_breaches(self):
        """Test get_domain_breaches convenience method."""
        hibp = HIBP(api_key="test-key")
        
        with responses_lib.RequestsMock() as rsps:
            rsps.add(
                responses_lib.GET,
                "https://haveibeenpwned.com/api/v3/breacheddomain/example.com",
                json={"user1": ["Adobe"]},
                status=200
            )
            
            result = hibp.get_domain_breaches("example.com")
            assert "user1" in result
    
    def test_get_subscribed_domains(self, sample_subscribed_domain_data):
        """Test get_subscribed_domains convenience method."""
        hibp = HIBP(api_key="test-key")
        
        with responses_lib.RequestsMock() as rsps:
            rsps.add(
                responses_lib.GET,
                "https://haveibeenpwned.com/api/v3/subscribeddomains",
                json=[sample_subscribed_domain_data],
                status=200
            )
            
            domains = hibp.get_subscribed_domains()
            assert len(domains) == 1
            assert isinstance(domains[0], SubscribedDomain)
    
    def test_get_stealer_logs_by_email(self):
        """Test get_stealer_logs_by_email convenience method."""
        hibp = HIBP(api_key="test-key")
        
        with responses_lib.RequestsMock() as rsps:
            rsps.add(
                responses_lib.GET,
                "https://haveibeenpwned.com/api/v3/stealerlogsbyemail/test%40example.com",
                json=["netflix.com"],
                status=200
            )
            
            domains = hibp.get_stealer_logs_by_email("test@example.com")
            assert domains == ["netflix.com"]
    
    def test_get_stealer_logs_by_website(self):
        """Test get_stealer_logs_by_website convenience method."""
        hibp = HIBP(api_key="test-key")
        
        with responses_lib.RequestsMock() as rsps:
            rsps.add(
                responses_lib.GET,
                "https://haveibeenpwned.com/api/v3/stealerlogsbywebsitedomain/netflix.com",
                json=["user@example.com"],
                status=200
            )
            
            emails = hibp.get_stealer_logs_by_website("netflix.com")
            assert "user@example.com" in emails
    
    def test_get_stealer_logs_by_email_domain(self):
        """Test get_stealer_logs_by_email_domain convenience method."""
        hibp = HIBP(api_key="test-key")
        
        with responses_lib.RequestsMock() as rsps:
            rsps.add(
                responses_lib.GET,
                "https://haveibeenpwned.com/api/v3/stealerlogsbyemaildomain/example.com",
                json={"user1": ["netflix.com"]},
                status=200
            )
            
            result = hibp.get_stealer_logs_by_email_domain("example.com")
            assert "user1" in result
    
    def test_get_account_pastes(self, sample_paste_data):
        """Test get_account_pastes convenience method."""
        hibp = HIBP(api_key="test-key")
        
        with responses_lib.RequestsMock() as rsps:
            rsps.add(
                responses_lib.GET,
                "https://haveibeenpwned.com/api/v3/pasteaccount/test%40example.com",
                json=[sample_paste_data],
                status=200
            )
            
            pastes = hibp.get_account_pastes("test@example.com")
            assert len(pastes) == 1
            assert isinstance(pastes[0], Paste)
    
    def test_get_subscription_status(self, sample_subscription_data):
        """Test get_subscription_status convenience method."""
        hibp = HIBP(api_key="test-key")
        
        with responses_lib.RequestsMock() as rsps:
            rsps.add(
                responses_lib.GET,
                "https://haveibeenpwned.com/api/v3/subscription/status",
                json=sample_subscription_data,
                status=200
            )
            
            subscription = hibp.get_subscription_status()
            assert isinstance(subscription, Subscription)
    
    def test_is_password_pwned(self, sample_password_hash_response):
        """Test is_password_pwned convenience method."""
        hibp = HIBP()
        
        with responses_lib.RequestsMock() as rsps:
            rsps.add(
                responses_lib.GET,
                "https://api.pwnedpasswords.com/range/5BAA6",
                body=sample_password_hash_response + "\n1E4C9B93F3F0682250B6CF8331B7EE68FD8:100",
                status=200
            )
            
            count = hibp.is_password_pwned("password")
            assert count == 100
    
    def test_search_password_hashes(self, sample_password_hash_response):
        """Test search_password_hashes convenience method."""
        hibp = HIBP()
        
        with responses_lib.RequestsMock() as rsps:
            rsps.add(
                responses_lib.GET,
                "https://api.pwnedpasswords.com/range/21BD1",
                body=sample_password_hash_response,
                status=200
            )
            
            results = hibp.search_password_hashes("21BD1")
            assert isinstance(results, dict)
            assert len(results) > 0


@pytest.mark.integration
class TestHIBPLive:
    """Test HIBP with live API."""
    
    def test_password_check_no_api_key(self):
        """Test password checking without API key."""
        hibp = HIBP()
        count = hibp.is_password_pwned("password")
        assert count > 0
    
    @skip_if_no_api_key()
    def test_breach_check_with_api_key(self, live_client):
        """Test breach checking with API key."""
        breaches = live_client.get_account_breaches(TEST_ACCOUNT_EXISTS)
        assert isinstance(breaches, list)
    
    def test_get_all_breaches_no_api_key(self):
        """Test getting all breaches without API key."""
        hibp = HIBP()
        breaches = hibp.get_all_breaches()
        assert len(breaches) > 0
    
    def test_get_data_classes_no_api_key(self):
        """Test getting data classes without API key."""
        hibp = HIBP()
        data_classes = hibp.get_data_classes()
        assert len(data_classes) > 0


@pytest.mark.unit
class TestHIBPParameterPassing:
    """Test that parameters are correctly passed through convenience methods."""
    
    def test_get_account_breaches_parameters(self, sample_breach_data):
        """Test that all parameters are passed correctly."""
        hibp = HIBP(api_key="test-key")
        
        with responses_lib.RequestsMock() as rsps:
            rsps.add(
                responses_lib.GET,
                "https://haveibeenpwned.com/api/v3/breachedaccount/test%40example.com",
                json=[sample_breach_data],
                status=200
            )
            
            breaches = hibp.get_account_breaches(
                "test@example.com",
                truncate_response=False,
                domain="adobe.com",
                include_unverified=False
            )
            
            # Check URL has correct parameters
            url = rsps.calls[0].request.url
            assert "truncateResponse=false" in url
            assert "domain=adobe.com" in url
            assert "includeUnverified=false" in url
    
    def test_is_password_pwned_parameters(self, sample_password_hash_response):
        """Test that password parameters are passed correctly."""
        hibp = HIBP()
        
        with responses_lib.RequestsMock() as rsps:
            rsps.add(
                responses_lib.GET,
                "https://api.pwnedpasswords.com/range/8846F",
                body=sample_password_hash_response,
                status=200
            )
            
            hibp.is_password_pwned("password", use_ntlm=True)
            assert "mode=ntlm" in rsps.calls[0].request.url
