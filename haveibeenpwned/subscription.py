"""
Subscription API endpoints.
"""

from .client import BaseClient
from .models import Subscription


class SubscriptionAPI:
    """API methods for subscription endpoints."""
    
    def __init__(self, client: BaseClient):
        self.client = client
    
    def get_status(self) -> Subscription:
        """
        Get the current subscription status.
        
        Returns:
            Subscription object with details about the current subscription
            
        Raises:
            AuthenticationError: If API key is invalid
        """
        data = self.client.get("subscription/status")
        return Subscription(data)
