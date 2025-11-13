"""
Breach-related API endpoints.
"""

from typing import List, Optional, Dict, Any

from .client import BaseClient
from .models import Breach, SubscribedDomain
from .exceptions import NotFoundError


class BreachAPI:
    """API methods for breach-related endpoints."""
    
    def __init__(self, client: BaseClient):
        self.client = client
    
    def get_breaches_for_account(
        self,
        account: str,
        truncate_response: bool = True,
        domain: Optional[str] = None,
        include_unverified: bool = True,
    ) -> List[Breach]:
        """
        Get all breaches for an account (email address, username, or phone number).
        
        Args:
            account: The account to search for
            truncate_response: Return only breach names (True) or full breach data (False)
            domain: Filter results to a specific domain
            include_unverified: Include unverified breaches in results
            
        Returns:
            List of Breach objects
            
        Raises:
            NotFoundError: If the account is not found in any breaches
            AuthenticationError: If API key is invalid
        """
        encoded_account = self.client.url_encode(account)
        params: Dict[str, Any] = {}
        
        if not truncate_response:
            params["truncateResponse"] = "false"
        
        if domain:
            params["domain"] = domain
        
        if not include_unverified:
            params["includeUnverified"] = "false"
        
        try:
            data = self.client.get(
                f"breachedaccount/{encoded_account}",
                params=params if params else None,
            )
            
            if data is None:
                return []
            
            return [Breach(breach_data) for breach_data in data]
        except NotFoundError:
            return []
    
    def get_all_breaches(
        self,
        domain: Optional[str] = None,
        is_spam_list: Optional[bool] = None,
    ) -> List[Breach]:
        """
        Get all breached sites in the system.
        
        Args:
            domain: Filter results to a specific domain
            is_spam_list: Filter to breaches that are/aren't spam lists
            
        Returns:
            List of all Breach objects
        """
        params: Dict[str, Any] = {}
        
        if domain:
            params["domain"] = domain
        
        if is_spam_list is not None:
            params["isSpamList"] = "true" if is_spam_list else "false"
        
        data = self.client.get(
            "breaches",
            params=params if params else None,
            include_api_key=False,
        )
        
        if data is None:
            return []
        
        return [Breach(breach_data) for breach_data in data]
    
    def get_breach(self, name: str) -> Breach:
        """
        Get a single breached site by name.
        
        Args:
            name: The breach name (e.g., "Adobe")
            
        Returns:
            Breach object
            
        Raises:
            NotFoundError: If the breach is not found
        """
        data = self.client.get(
            f"breach/{name}",
            include_api_key=False,
        )
        
        return Breach(data)
    
    def get_latest_breach(self) -> Breach:
        """
        Get the most recently added breach.
        
        Returns:
            Breach object
        """
        data = self.client.get(
            "latestbreach",
            include_api_key=False,
        )
        
        return Breach(data)
    
    def get_data_classes(self) -> List[str]:
        """
        Get all data classes in the system.
        
        Returns:
            List of data class names (e.g., ["Email addresses", "Passwords"])
        """
        data = self.client.get(
            "dataclasses",
            include_api_key=False,
        )
        
        return data if data else []
    
    def get_breached_domain(self, domain: str) -> Dict[str, List[str]]:
        """
        Get all breached email addresses for a domain.
        
        Args:
            domain: The domain to search (must be verified in your account)
            
        Returns:
            Dictionary mapping email aliases to lists of breach names
            Example: {"alias1": ["Adobe"], "alias2": ["Adobe", "LinkedIn"]}
            
        Raises:
            NotFoundError: If no breaches found for the domain
            AuthenticationError: If API key is invalid or domain not verified
        """
        try:
            data = self.client.get(f"breacheddomain/{domain}")
            return data if data else {}
        except NotFoundError:
            return {}
    
    def get_subscribed_domains(self) -> List[SubscribedDomain]:
        """
        Get all domains subscribed to domain search.
        
        Returns:
            List of SubscribedDomain objects
            
        Raises:
            AuthenticationError: If API key is invalid
        """
        data = self.client.get("subscribeddomains")
        
        if data is None:
            return []
        
        return [SubscribedDomain(domain_data) for domain_data in data]
