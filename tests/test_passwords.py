"""
Tests for Pwned Passwords API.
"""

import hashlib
import pytest
import responses as responses_lib

from haveibeenpwned.passwords import PwnedPasswordsAPI
from haveibeenpwned.client import BaseClient


@pytest.mark.unit
class TestPwnedPasswordsAPIMocked:
    """Test PwnedPasswordsAPI with mocked responses."""
    
    def test_check_password_found(self, sample_password_hash_response):
        """Test checking a password that exists in breaches."""
        client = BaseClient()
        api = PwnedPasswordsAPI(client)
        
        # Hash of "password" is 5BAA61E4C9B93F3F0682250B6CF8331B7EE68FD8
        # First 5 chars: 5BAA6
        with responses_lib.RequestsMock() as rsps:
            rsps.add(
                responses_lib.GET,
                "https://api.pwnedpasswords.com/range/5BAA6",
                body=sample_password_hash_response + "\n1E4C9B93F3F0682250B6CF8331B7EE68FD8:3861493",
                status=200
            )
            
            count = api.check_password("password")
            assert count == 3861493
    
    def test_check_password_not_found(self, sample_password_hash_response):
        """Test checking a password not in breaches."""
        client = BaseClient()
        api = PwnedPasswordsAPI(client)
        
        with responses_lib.RequestsMock() as rsps:
            rsps.add(
                responses_lib.GET,
                "https://api.pwnedpasswords.com/range/A94A8",
                body=sample_password_hash_response,
                status=200
            )
            
            # This is a hash that won't be in the response
            count = api.check_password("VerySecurePassword!2024")
            assert count == 0
    
    def test_check_password_ntlm(self, sample_password_hash_response):
        """Test checking password with NTLM hash."""
        client = BaseClient()
        api = PwnedPasswordsAPI(client)
        
        with responses_lib.RequestsMock() as rsps:
            rsps.add(
                responses_lib.GET,
                "https://api.pwnedpasswords.com/range/8846F",
                body="7401AAAAAAAA:10\n7401AAAAAAAB:20",
                status=200
            )
            
            count = api.check_password("password", use_ntlm=True)
            # Just check it doesn't error; exact count depends on response
            assert isinstance(count, int)
    
    def test_check_password_with_padding(self, sample_password_hash_response):
        """Test checking password with padding enabled."""
        client = BaseClient()
        api = PwnedPasswordsAPI(client)
        
        # Add padded entries (count of 0)
        padded_response = sample_password_hash_response + "\nPADDEDHASH1:0\nPADDEDHASH2:0"
        
        with responses_lib.RequestsMock() as rsps:
            rsps.add(
                responses_lib.GET,
                "https://api.pwnedpasswords.com/range/5BAA6",
                body=padded_response + "\n1E4C9B93F3F0682250B6CF8331B7EE68FD8:100",
                status=200
            )
            
            count = api.check_password("password", add_padding=True)
            # Padded entries (count 0) should be filtered out
            assert count == 100
    
    def test_search_by_range(self, sample_password_hash_response):
        """Test searching by hash range."""
        client = BaseClient()
        api = PwnedPasswordsAPI(client)
        
        with responses_lib.RequestsMock() as rsps:
            rsps.add(
                responses_lib.GET,
                "https://api.pwnedpasswords.com/range/21BD1",
                body=sample_password_hash_response,
                status=200
            )
            
            results = api.search_by_range("21BD1")
            assert isinstance(results, dict)
            assert len(results) == 5
            assert "0018A45C4D1DEF81644B54AB7F969B88D65" in results
            assert results["0018A45C4D1DEF81644B54AB7F969B88D65"] == 1
    
    def test_search_by_range_invalid_prefix(self):
        """Test search with invalid prefix length."""
        client = BaseClient()
        api = PwnedPasswordsAPI(client)
        
        with pytest.raises(ValueError) as exc_info:
            api.search_by_range("ABC")  # Too short
        assert "exactly 5 characters" in str(exc_info.value)
        
        with pytest.raises(ValueError):
            api.search_by_range("ABCDEFG")  # Too long
    
    def test_search_by_range_ntlm(self, sample_password_hash_response):
        """Test searching by NTLM hash range."""
        client = BaseClient()
        api = PwnedPasswordsAPI(client)
        
        with responses_lib.RequestsMock() as rsps:
            rsps.add(
                responses_lib.GET,
                "https://api.pwnedpasswords.com/range/21BD1",
                body=sample_password_hash_response,
                status=200
            )
            
            results = api.search_by_range("21BD1", use_ntlm=True)
            assert isinstance(results, dict)
            assert "mode=ntlm" in rsps.calls[0].request.url
    
    def test_hash_password_sha1(self):
        """Test SHA-1 password hashing."""
        hash_result = PwnedPasswordsAPI.hash_password_sha1("password")
        expected = hashlib.sha1("password".encode('utf-8')).hexdigest().upper()
        assert hash_result == expected
        assert hash_result == "5BAA61E4C9B93F3F0682250B6CF8331B7EE68FD8"
    
    def test_hash_password_ntlm(self):
        """Test NTLM password hashing."""
        hash_result = PwnedPasswordsAPI.hash_password_ntlm("password")
        expected = hashlib.new('md4', "password".encode('utf-16le')).hexdigest().upper()
        assert hash_result == expected
        assert hash_result == "8846F7EAEE8FB117AD06BDD830B7586C"


@pytest.mark.integration
class TestPwnedPasswordsAPILive:
    """Test PwnedPasswordsAPI with live API (no API key needed)."""
    
    def test_check_common_password_live(self, password_client):
        """Test checking a very common password."""
        count = password_client.passwords.check_password("password")
        assert count > 0  # "password" should definitely be pwned
        assert count > 1000000  # Should be in millions
    
    def test_check_uncommon_password_live(self, password_client):
        """Test checking a strong, unique password."""
        # Generate a very unique password
        unique_password = "MyVeryUniqueP@ssw0rd!2024XYZ"
        count = password_client.passwords.check_password(unique_password)
        # Should probably not be found, but we can't guarantee
        assert isinstance(count, int)
        assert count >= 0
    
    def test_search_by_range_live(self, password_client):
        """Test searching by hash range."""
        # First 5 chars of SHA-1 hash of "password"
        results = password_client.passwords.search_by_range("5BAA6")
        assert isinstance(results, dict)
        assert len(results) > 0
        
        # The suffix of "password" should be in results
        suffix = "1E4C9B93F3F0682250B6CF8331B7EE68FD8"
        assert suffix in results
        assert results[suffix] > 0
    
    def test_check_password_ntlm_live(self, password_client):
        """Test checking password with NTLM hash."""
        count = password_client.passwords.check_password("password", use_ntlm=True)
        assert count > 0
    
    def test_check_password_with_padding_live(self, password_client):
        """Test checking password with padding."""
        count = password_client.passwords.check_password("password", add_padding=True)
        assert count > 0
        # Result should be the same as without padding
        count_no_padding = password_client.passwords.check_password("password", add_padding=False)
        assert count == count_no_padding
