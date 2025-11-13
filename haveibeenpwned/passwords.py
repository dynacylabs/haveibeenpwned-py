"""
Pwned Passwords API endpoints.
"""

import hashlib
from typing import Dict, Optional

from .client import BaseClient


class PwnedPasswordsAPI:
    """API methods for Pwned Passwords endpoints."""
    
    def __init__(self, client: BaseClient):
        self.client = client
    
    def check_password(
        self,
        password: str,
        use_ntlm: bool = False,
        add_padding: bool = False,
    ) -> int:
        """
        Check if a password has been pwned.
        
        Uses k-Anonymity to protect the password being checked.
        
        Args:
            password: The password to check
            use_ntlm: Use NTLM hash instead of SHA-1
            add_padding: Add padding to the response for enhanced privacy
            
        Returns:
            Number of times the password has been seen in breaches (0 if not found)
        """
        # Hash the password
        if use_ntlm:
            hash_obj = hashlib.new('md4', password.encode('utf-16le'))
        else:
            hash_obj = hashlib.sha1(password.encode('utf-8'))
        
        password_hash = hash_obj.hexdigest().upper()
        
        # Use k-Anonymity: send first 5 characters, get suffixes back
        prefix = password_hash[:5]
        suffix = password_hash[5:]
        
        # Search for the suffix in the results
        results = self.search_by_range(prefix, use_ntlm=use_ntlm, add_padding=add_padding)
        
        return results.get(suffix, 0)
    
    def search_by_range(
        self,
        hash_prefix: str,
        use_ntlm: bool = False,
        add_padding: bool = False,
    ) -> Dict[str, int]:
        """
        Search for password hashes by prefix (k-Anonymity model).
        
        Args:
            hash_prefix: First 5 characters of the hash (SHA-1 or NTLM)
            use_ntlm: Use NTLM hash mode instead of SHA-1
            add_padding: Add padding to the response for enhanced privacy
            
        Returns:
            Dictionary mapping hash suffixes to occurrence counts
        """
        if len(hash_prefix) != 5:
            raise ValueError("Hash prefix must be exactly 5 characters")
        
        params = {}
        if use_ntlm:
            params["mode"] = "ntlm"
        
        # Add padding header if requested
        headers = {}
        if add_padding:
            headers["Add-Padding"] = "true"
        
        # Use the Pwned Passwords API base URL
        endpoint = f"range/{hash_prefix.upper()}"
        
        # Make request with custom headers if needed
        if add_padding:
            # We need to use the session directly to add custom headers
            url = f"{self.client.PWNED_PASSWORDS_URL}/{endpoint}"
            base_headers = self.client._get_headers(include_api_key=False)
            base_headers.update(headers)
            
            response = self.client.session.get(
                url,
                headers=base_headers,
                params=params if params else None,
                timeout=self.client.timeout,
            )
            
            data = self.client._handle_response(response)
            text = response.text if response.status_code == 200 else ""
        else:
            response = self.client.session.get(
                f"{self.client.PWNED_PASSWORDS_URL}/{endpoint}",
                headers=self.client._get_headers(include_api_key=False),
                params=params if params else None,
                timeout=self.client.timeout,
            )
            text = response.text if response.status_code == 200 else ""
        
        # Parse the response
        results = {}
        if text:
            for line in text.strip().split('\n'):
                if ':' in line:
                    suffix, count = line.split(':', 1)
                    count_int = int(count)
                    # Skip padded entries (count of 0)
                    if add_padding and count_int == 0:
                        continue
                    results[suffix.strip()] = count_int
        
        return results
    
    @staticmethod
    def hash_password_sha1(password: str) -> str:
        """
        Generate SHA-1 hash of a password.
        
        Args:
            password: The password to hash
            
        Returns:
            Uppercase SHA-1 hash
        """
        return hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    
    @staticmethod
    def hash_password_ntlm(password: str) -> str:
        """
        Generate NTLM hash of a password.
        
        Args:
            password: The password to hash
            
        Returns:
            Uppercase NTLM hash
        """
        return hashlib.new('md4', password.encode('utf-16le')).hexdigest().upper()
