"""
Tests for data models.
"""

import pytest
from haveibeenpwned.models import Breach, Paste, Subscription, SubscribedDomain


@pytest.mark.unit
class TestBreachModel:
    """Test Breach model."""
    
    def test_breach_initialization(self, sample_breach_data):
        """Test breach initialization with full data."""
        breach = Breach(sample_breach_data)
        
        assert breach.name == "Adobe"
        assert breach.title == "Adobe"
        assert breach.domain == "adobe.com"
        assert breach.breach_date == "2013-10-04"
        assert breach.added_date == "2013-12-04T00:00:00Z"
        assert breach.modified_date == "2022-05-15T23:52:49Z"
        assert breach.pwn_count == 152445165
        assert "153 million Adobe accounts" in breach.description
        assert breach.logo_path == "Adobe.png"
        assert "Email addresses" in breach.data_classes
        assert breach.is_verified is True
        assert breach.is_fabricated is False
        assert breach.is_sensitive is False
        assert breach.is_retired is False
        assert breach.is_spam_list is False
        assert breach.is_malware is False
        assert breach.is_stealer_log is False
        assert breach.is_subscription_free is False
        assert breach.attribution is None
    
    def test_breach_truncated(self, sample_breach_truncated):
        """Test breach initialization with truncated data."""
        breach = Breach(sample_breach_truncated)
        
        assert breach.name == "Adobe"
        assert breach.title == ""
        assert breach.pwn_count == 0
        assert breach.data_classes == []
    
    def test_breach_repr(self, sample_breach_data):
        """Test breach string representation."""
        breach = Breach(sample_breach_data)
        assert "Adobe" in repr(breach)
        assert "152445165" in repr(breach)
    
    def test_breach_to_dict(self, sample_breach_data):
        """Test breach to_dict conversion."""
        breach = Breach(sample_breach_data)
        breach_dict = breach.to_dict()
        
        assert breach_dict["Name"] == "Adobe"
        assert breach_dict["Domain"] == "adobe.com"
        assert breach_dict["PwnCount"] == 152445165
        assert isinstance(breach_dict["DataClasses"], list)
    
    def test_breach_empty_data(self):
        """Test breach with empty data."""
        breach = Breach({})
        assert breach.name == ""
        assert breach.pwn_count == 0
        assert breach.data_classes == []


@pytest.mark.unit
class TestPasteModel:
    """Test Paste model."""
    
    def test_paste_initialization(self, sample_paste_data):
        """Test paste initialization."""
        paste = Paste(sample_paste_data)
        
        assert paste.source == "Pastebin"
        assert paste.id == "8Q0BvKD8"
        assert paste.title == "syslog"
        assert paste.date == "2014-03-04T19:14:54Z"
        assert paste.email_count == 139
    
    def test_paste_no_title(self):
        """Test paste without title."""
        data = {
            "Source": "Pastie",
            "Id": "12345",
            "Date": "2014-01-01T00:00:00Z",
            "EmailCount": 10
        }
        paste = Paste(data)
        
        assert paste.source == "Pastie"
        assert paste.title is None
    
    def test_paste_repr(self, sample_paste_data):
        """Test paste string representation."""
        paste = Paste(sample_paste_data)
        assert "Pastebin" in repr(paste)
        assert "8Q0BvKD8" in repr(paste)
        assert "139" in repr(paste)
    
    def test_paste_to_dict(self, sample_paste_data):
        """Test paste to_dict conversion."""
        paste = Paste(sample_paste_data)
        paste_dict = paste.to_dict()
        
        assert paste_dict["Source"] == "Pastebin"
        assert paste_dict["Id"] == "8Q0BvKD8"
        assert paste_dict["EmailCount"] == 139


@pytest.mark.unit
class TestSubscriptionModel:
    """Test Subscription model."""
    
    def test_subscription_initialization(self, sample_subscription_data):
        """Test subscription initialization."""
        subscription = Subscription(sample_subscription_data)
        
        assert subscription.subscription_name == "Pwned 1"
        assert subscription.description == "Up to 10 passwords per minute"
        assert subscription.subscribed_until == "2024-12-31T23:59:59Z"
        assert subscription.rpm == 10
        assert subscription.domain_search_max_breached_accounts == 100
        assert subscription.includes_stealer_logs is False
    
    def test_subscription_repr(self, sample_subscription_data):
        """Test subscription string representation."""
        subscription = Subscription(sample_subscription_data)
        assert "Pwned 1" in repr(subscription)
        assert "10" in repr(subscription)
    
    def test_subscription_to_dict(self, sample_subscription_data):
        """Test subscription to_dict conversion."""
        subscription = Subscription(sample_subscription_data)
        sub_dict = subscription.to_dict()
        
        assert sub_dict["SubscriptionName"] == "Pwned 1"
        assert sub_dict["Rpm"] == 10
        assert sub_dict["IncludesStealerLogs"] is False


@pytest.mark.unit
class TestSubscribedDomainModel:
    """Test SubscribedDomain model."""
    
    def test_subscribed_domain_initialization(self, sample_subscribed_domain_data):
        """Test subscribed domain initialization."""
        domain = SubscribedDomain(sample_subscribed_domain_data)
        
        assert domain.domain_name == "example.com"
        assert domain.pwn_count == 150
        assert domain.pwn_count_excluding_spam_lists == 120
        assert domain.pwn_count_excluding_spam_lists_at_last_subscription_renewal == 100
        assert domain.next_subscription_renewal == "2024-12-31T23:59:59Z"
    
    def test_subscribed_domain_null_values(self):
        """Test subscribed domain with null values."""
        data = {"DomainName": "test.com"}
        domain = SubscribedDomain(data)
        
        assert domain.domain_name == "test.com"
        assert domain.pwn_count is None
        assert domain.pwn_count_excluding_spam_lists is None
    
    def test_subscribed_domain_repr(self, sample_subscribed_domain_data):
        """Test subscribed domain string representation."""
        domain = SubscribedDomain(sample_subscribed_domain_data)
        assert "example.com" in repr(domain)
        assert "150" in repr(domain)
    
    def test_subscribed_domain_to_dict(self, sample_subscribed_domain_data):
        """Test subscribed domain to_dict conversion."""
        domain = SubscribedDomain(sample_subscribed_domain_data)
        domain_dict = domain.to_dict()
        
        assert domain_dict["DomainName"] == "example.com"
        assert domain_dict["PwnCount"] == 150
