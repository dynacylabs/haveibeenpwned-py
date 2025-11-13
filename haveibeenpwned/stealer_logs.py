"""
Stealer logs API endpoints.
"""

from typing import List, Dict

from .client import BaseClient
from .exceptions import NotFoundError


class StealerLogsAPI:
    """API methods for stealer logs endpoints."""
    
    def __init__(self, client: BaseClient):
        self.client = client
    
    def get_by_email(self, email: str) -> List[str]:
        """
        Get all stealer log domains for an email address.
        
        This returns website domains where the email address was captured by an info stealer.
        
        Args:
            email: The email address to search for (must be on a verified domain)
            
        Returns:
            List of website domains (e.g., ["netflix.com", "spotify.com"])
            
        Raises:
            NotFoundError: If no stealer log entries found
            AuthenticationError: If API key is invalid or domain not verified
        """
        encoded_email = self.client.url_encode(email)
        
        try:
            data = self.client.get(f"stealerlogsbyemail/{encoded_email}")
            return data if data else []
        except NotFoundError:
            return []
    
    def get_by_website_domain(self, domain: str) -> List[str]:
        """
        Get all stealer log email addresses for a website domain.
        
        This returns email addresses captured when users authenticated to the specified domain.
        
        Args:
            domain: The website domain to search for (must be verified in your account)
            
        Returns:
            List of email addresses (e.g., ["user1@example.com", "user2@example.com"])
            
        Raises:
            NotFoundError: If no stealer log entries found
            AuthenticationError: If API key is invalid or domain not verified
        """
        try:
            data = self.client.get(f"stealerlogsbywebsitedomain/{domain}")
            return data if data else []
        except NotFoundError:
            return []
    
    def get_by_email_domain(self, domain: str) -> Dict[str, List[str]]:
        """
        Get all stealer log email aliases for an email domain.
        
        This returns email aliases on the domain and the websites where they were captured.
        
        Args:
            domain: The email domain to search for (must be verified in your account)
            
        Returns:
            Dictionary mapping email aliases to lists of website domains
            Example: {"user1": ["netflix.com"], "user2": ["netflix.com", "spotify.com"]}
            
        Raises:
            NotFoundError: If no stealer log entries found
            AuthenticationError: If API key is invalid or domain not verified
        """
        try:
            data = self.client.get(f"stealerlogsbyemaildomain/{domain}")
            return data if data else {}
        except NotFoundError:
            return {}
