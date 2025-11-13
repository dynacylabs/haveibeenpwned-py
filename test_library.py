"""
Simple test to verify the library installation and basic functionality.
"""

import sys


def test_import():
    """Test that the library can be imported."""
    try:
        from haveibeenpwned import HIBP
        print("✓ Successfully imported HIBP")
        return True
    except ImportError as e:
        print(f"✗ Failed to import: {e}")
        return False


def test_models():
    """Test that models can be imported."""
    try:
        from haveibeenpwned import Breach, Paste, Subscription, SubscribedDomain
        print("✓ Successfully imported models")
        return True
    except ImportError as e:
        print(f"✗ Failed to import models: {e}")
        return False


def test_exceptions():
    """Test that exceptions can be imported."""
    try:
        from haveibeenpwned import (
            HIBPError,
            AuthenticationError,
            BadRequestError,
            RateLimitError,
            NotFoundError,
            ForbiddenError,
            ServiceUnavailableError,
        )
        print("✓ Successfully imported exceptions")
        return True
    except ImportError as e:
        print(f"✗ Failed to import exceptions: {e}")
        return False


def test_client_initialization():
    """Test that the client can be initialized."""
    try:
        from haveibeenpwned import HIBP
        
        # Test without API key
        hibp = HIBP()
        print("✓ Client initialized without API key")
        
        # Test with API key
        hibp = HIBP(api_key="test-key")
        print("✓ Client initialized with API key")
        
        # Test custom user agent
        hibp = HIBP(user_agent="test-agent")
        print("✓ Client initialized with custom user agent")
        
        return True
    except Exception as e:
        print(f"✗ Failed to initialize client: {e}")
        return False


def test_pwned_passwords():
    """Test Pwned Passwords API (no API key needed)."""
    try:
        from haveibeenpwned import HIBP
        
        hibp = HIBP()
        
        # Check a known pwned password
        count = hibp.is_password_pwned("password")
        if count > 0:
            print(f"✓ Pwned password check works (found {count:,} times)")
        else:
            print("⚠ Warning: 'password' should be in breach database")
        
        # Check password hash search
        results = hibp.search_password_hashes("21BD1")
        if len(results) > 0:
            print(f"✓ Hash search works (found {len(results)} results)")
        else:
            print("✗ Hash search returned no results")
            return False
        
        return True
    except Exception as e:
        print(f"✗ Pwned Passwords test failed: {e}")
        return False


def main():
    """Run all tests."""
    print("=" * 60)
    print("Testing Have I Been Pwned Library")
    print("=" * 60)
    print()
    
    tests = [
        ("Import Test", test_import),
        ("Models Import Test", test_models),
        ("Exceptions Import Test", test_exceptions),
        ("Client Initialization Test", test_client_initialization),
        ("Pwned Passwords Test", test_pwned_passwords),
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n{test_name}:")
        print("-" * 60)
        results.append(test_func())
    
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    passed = sum(results)
    total = len(results)
    print(f"Passed: {passed}/{total}")
    
    if passed == total:
        print("✓ All tests passed!")
        return 0
    else:
        print(f"✗ {total - passed} test(s) failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())
