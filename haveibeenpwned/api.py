"""
Main API interface for Have I Been Pwned.
"""

from typing import List, Optional, Dict

from .client import BaseClient
from .breach import BreachAPI
from .stealer_logs import StealerLogsAPI
from .pastes import PastesAPI
from .subscription import SubscriptionAPI
from .passwords import PwnedPasswordsAPI
from .models import Breach, Paste, Subscription, SubscribedDomain


class HIBP:
    """
    Main interface for the Have I Been Pwned API.
    
    This class provides a simple, unified interface to all HIBP API endpoints.
    
    Example:
        >>> hibp = HIBP(api_key="your-api-key")
        >>> breaches = hibp.get_account_breaches("test@example.com")
        >>> pwned_count = hibp.is_password_pwned("password123")
    """
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        user_agent: str = "haveibeenpwned-python-client",
        timeout: int = 30,
    ):
        """
        Initialize the HIBP API client.
        
        Args:
            api_key: HIBP API key for authenticated endpoints (not needed for Pwned Passwords)
            user_agent: User agent string for API requests
            timeout: Request timeout in seconds
        """
        self.client = BaseClient(api_key=api_key, user_agent=user_agent, timeout=timeout)
        
        # Initialize API modules
        self.breaches = BreachAPI(self.client)
        self.stealer_logs = StealerLogsAPI(self.client)
        self.pastes = PastesAPI(self.client)
        self.subscription = SubscriptionAPI(self.client)
        self.passwords = PwnedPasswordsAPI(self.client)
    
    # Convenience methods for common operations
    
    def get_account_breaches(
        self,
        account: str,
        truncate_response: bool = True,
        domain: Optional[str] = None,
        include_unverified: bool = True,
    ) -> List[Breach]:
        """
        Get all breaches for an account.
        
        Args:
            account: Email address, username, or phone number
            truncate_response: Return only breach names (True) or full data (False)
            domain: Filter to specific domain
            include_unverified: Include unverified breaches
            
        Returns:
            List of Breach objects
        """
        return self.breaches.get_breaches_for_account(
            account=account,
            truncate_response=truncate_response,
            domain=domain,
            include_unverified=include_unverified,
        )
    
    def get_all_breaches(
        self,
        domain: Optional[str] = None,
        is_spam_list: Optional[bool] = None,
    ) -> List[Breach]:
        """
        Get all breached sites in the system.
        
        Args:
            domain: Filter to specific domain
            is_spam_list: Filter to spam lists (True) or non-spam lists (False)
            
        Returns:
            List of all Breach objects
        """
        return self.breaches.get_all_breaches(domain=domain, is_spam_list=is_spam_list)
    
    def get_breach(self, name: str) -> Breach:
        """
        Get a single breach by name.
        
        Args:
            name: Breach name (e.g., "Adobe")
            
        Returns:
            Breach object
        """
        return self.breaches.get_breach(name)
    
    def get_latest_breach(self) -> Breach:
        """
        Get the most recently added breach.
        
        Returns:
            Breach object
        """
        return self.breaches.get_latest_breach()
    
    def get_data_classes(self) -> List[str]:
        """
        Get all data classes in the system.
        
        Returns:
            List of data class names
        """
        return self.breaches.get_data_classes()
    
    def get_domain_breaches(self, domain: str) -> Dict[str, List[str]]:
        """
        Get all breached email addresses for a domain.
        
        Args:
            domain: Domain to search (must be verified)
            
        Returns:
            Dictionary mapping email aliases to breach names
        """
        return self.breaches.get_breached_domain(domain)
    
    def get_subscribed_domains(self) -> List[SubscribedDomain]:
        """
        Get all subscribed domains.
        
        Returns:
            List of SubscribedDomain objects
        """
        return self.breaches.get_subscribed_domains()
    
    def get_stealer_logs_by_email(self, email: str) -> List[str]:
        """
        Get stealer log domains for an email address.
        
        Args:
            email: Email address to search
            
        Returns:
            List of website domains
        """
        return self.stealer_logs.get_by_email(email)
    
    def get_stealer_logs_by_website(self, domain: str) -> List[str]:
        """
        Get stealer log email addresses for a website domain.
        
        Args:
            domain: Website domain to search
            
        Returns:
            List of email addresses
        """
        return self.stealer_logs.get_by_website_domain(domain)
    
    def get_stealer_logs_by_email_domain(self, domain: str) -> Dict[str, List[str]]:
        """
        Get stealer log email aliases for an email domain.
        
        Args:
            domain: Email domain to search
            
        Returns:
            Dictionary mapping aliases to website domains
        """
        return self.stealer_logs.get_by_email_domain(domain)
    
    def get_account_pastes(self, account: str) -> List[Paste]:
        """
        Get all pastes for an account.
        
        Args:
            account: Email address to search
            
        Returns:
            List of Paste objects
        """
        return self.pastes.get_pastes_for_account(account)
    
    def get_subscription_status(self) -> Subscription:
        """
        Get subscription status.
        
        Returns:
            Subscription object
        """
        return self.subscription.get_status()
    
    def is_password_pwned(
        self,
        password: str,
        use_ntlm: bool = False,
        add_padding: bool = False,
    ) -> int:
        """
        Check if a password has been pwned.
        
        Args:
            password: Password to check
            use_ntlm: Use NTLM hash instead of SHA-1
            add_padding: Add padding for enhanced privacy
            
        Returns:
            Number of times the password has been seen (0 if not pwned)
        """
        return self.passwords.check_password(
            password=password,
            use_ntlm=use_ntlm,
            add_padding=add_padding,
        )
    
    def search_password_hashes(
        self,
        hash_prefix: str,
        use_ntlm: bool = False,
        add_padding: bool = False,
    ) -> Dict[str, int]:
        """
        Search for password hashes by prefix.
        
        Args:
            hash_prefix: First 5 characters of hash
            use_ntlm: Use NTLM hash mode
            add_padding: Add padding for enhanced privacy
            
        Returns:
            Dictionary of hash suffixes to counts
        """
        return self.passwords.search_by_range(
            hash_prefix=hash_prefix,
            use_ntlm=use_ntlm,
            add_padding=add_padding,
        )
