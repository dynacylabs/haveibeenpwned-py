"""
Pastes API endpoints.
"""

from typing import List

from .client import BaseClient
from .models import Paste
from .exceptions import NotFoundError


class PastesAPI:
    """API methods for pastes endpoints."""
    
    def __init__(self, client: BaseClient):
        self.client = client
    
    def get_pastes_for_account(self, account: str) -> List[Paste]:
        """
        Get all pastes for an account (email address).
        
        Args:
            account: The email address to search for
            
        Returns:
            List of Paste objects
            
        Raises:
            NotFoundError: If no pastes found for the account
            AuthenticationError: If API key is invalid
        """
        encoded_account = self.client.url_encode(account)
        
        try:
            data = self.client.get(f"pasteaccount/{encoded_account}")
            
            if data is None:
                return []
            
            return [Paste(paste_data) for paste_data in data]
        except NotFoundError:
            return []
