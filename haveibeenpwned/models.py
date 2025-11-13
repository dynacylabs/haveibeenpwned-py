"""
Data models for Have I Been Pwned API responses.
"""

from typing import List, Optional
from datetime import datetime


class Breach:
    """Represents a data breach."""
    
    def __init__(self, data: dict):
        self.name: str = data.get("Name", "")
        self.title: str = data.get("Title", "")
        self.domain: str = data.get("Domain", "")
        self.breach_date: Optional[str] = data.get("BreachDate")
        self.added_date: Optional[str] = data.get("AddedDate")
        self.modified_date: Optional[str] = data.get("ModifiedDate")
        self.pwn_count: int = data.get("PwnCount", 0)
        self.description: str = data.get("Description", "")
        self.logo_path: str = data.get("LogoPath", "")
        self.data_classes: List[str] = data.get("DataClasses", [])
        self.is_verified: bool = data.get("IsVerified", False)
        self.is_fabricated: bool = data.get("IsFabricated", False)
        self.is_sensitive: bool = data.get("IsSensitive", False)
        self.is_retired: bool = data.get("IsRetired", False)
        self.is_spam_list: bool = data.get("IsSpamList", False)
        self.is_malware: bool = data.get("IsMalware", False)
        self.is_stealer_log: bool = data.get("IsStealerLog", False)
        self.is_subscription_free: bool = data.get("IsSubscriptionFree", False)
        self.attribution: Optional[str] = data.get("Attribution")
        
    def __repr__(self):
        return f"<Breach: {self.name} ({self.pwn_count} accounts)>"
    
    def to_dict(self) -> dict:
        """Convert the breach object to a dictionary."""
        return {
            "Name": self.name,
            "Title": self.title,
            "Domain": self.domain,
            "BreachDate": self.breach_date,
            "AddedDate": self.added_date,
            "ModifiedDate": self.modified_date,
            "PwnCount": self.pwn_count,
            "Description": self.description,
            "LogoPath": self.logo_path,
            "DataClasses": self.data_classes,
            "IsVerified": self.is_verified,
            "IsFabricated": self.is_fabricated,
            "IsSensitive": self.is_sensitive,
            "IsRetired": self.is_retired,
            "IsSpamList": self.is_spam_list,
            "IsMalware": self.is_malware,
            "IsStealerLog": self.is_stealer_log,
            "IsSubscriptionFree": self.is_subscription_free,
            "Attribution": self.attribution,
        }


class Paste:
    """Represents a paste containing breached data."""
    
    def __init__(self, data: dict):
        self.source: str = data.get("Source", "")
        self.id: str = data.get("Id", "")
        self.title: Optional[str] = data.get("Title")
        self.date: Optional[str] = data.get("Date")
        self.email_count: int = data.get("EmailCount", 0)
        
    def __repr__(self):
        return f"<Paste: {self.source}/{self.id} ({self.email_count} emails)>"
    
    def to_dict(self) -> dict:
        """Convert the paste object to a dictionary."""
        return {
            "Source": self.source,
            "Id": self.id,
            "Title": self.title,
            "Date": self.date,
            "EmailCount": self.email_count,
        }


class Subscription:
    """Represents subscription status information."""
    
    def __init__(self, data: dict):
        self.subscription_name: str = data.get("SubscriptionName", "")
        self.description: str = data.get("Description", "")
        self.subscribed_until: Optional[str] = data.get("SubscribedUntil")
        self.rpm: int = data.get("Rpm", 0)
        self.domain_search_max_breached_accounts: int = data.get("DomainSearchMaxBreachedAccounts", 0)
        self.includes_stealer_logs: bool = data.get("IncludesStealerLogs", False)
        
    def __repr__(self):
        return f"<Subscription: {self.subscription_name} (RPM: {self.rpm})>"
    
    def to_dict(self) -> dict:
        """Convert the subscription object to a dictionary."""
        return {
            "SubscriptionName": self.subscription_name,
            "Description": self.description,
            "SubscribedUntil": self.subscribed_until,
            "Rpm": self.rpm,
            "DomainSearchMaxBreachedAccounts": self.domain_search_max_breached_accounts,
            "IncludesStealerLogs": self.includes_stealer_logs,
        }


class SubscribedDomain:
    """Represents a subscribed domain."""
    
    def __init__(self, data: dict):
        self.domain_name: str = data.get("DomainName", "")
        self.pwn_count: Optional[int] = data.get("PwnCount")
        self.pwn_count_excluding_spam_lists: Optional[int] = data.get("PwnCountExcludingSpamLists")
        self.pwn_count_excluding_spam_lists_at_last_subscription_renewal: Optional[int] = data.get(
            "PwnCountExcludingSpamListsAtLastSubscriptionRenewal"
        )
        self.next_subscription_renewal: Optional[str] = data.get("NextSubscriptionRenewal")
        
    def __repr__(self):
        return f"<SubscribedDomain: {self.domain_name} ({self.pwn_count} breaches)>"
    
    def to_dict(self) -> dict:
        """Convert the subscribed domain object to a dictionary."""
        return {
            "DomainName": self.domain_name,
            "PwnCount": self.pwn_count,
            "PwnCountExcludingSpamLists": self.pwn_count_excluding_spam_lists,
            "PwnCountExcludingSpamListsAtLastSubscriptionRenewal": 
                self.pwn_count_excluding_spam_lists_at_last_subscription_renewal,
            "NextSubscriptionRenewal": self.next_subscription_renewal,
        }
