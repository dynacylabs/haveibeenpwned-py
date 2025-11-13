"""
Comprehensive example showing all library features.
"""

from haveibeenpwned import (
    HIBP,
    NotFoundError,
    RateLimitError,
    AuthenticationError,
)


def demonstrate_breaches_api():
    """Demonstrate breach-related API calls."""
    print("\n" + "=" * 70)
    print("BREACHES API")
    print("=" * 70)
    
    # Use test API key
    hibp = HIBP(api_key="00000000000000000000000000000000")
    
    # 1. Get breaches for account
    print("\n1. Get breaches for an account:")
    try:
        breaches = hibp.get_account_breaches("account-exists@hibp-integration-tests.com")
        print(f"   Found {len(breaches)} breach(es)")
        for breach in breaches[:2]:
            print(f"   - {breach.name}")
    except NotFoundError:
        print("   No breaches found")
    
    # 2. Get all breaches
    print("\n2. Get all breaches in the system:")
    all_breaches = hibp.get_all_breaches()
    print(f"   Total: {len(all_breaches)} breaches")
    print(f"   Examples: {', '.join([b.name for b in all_breaches[:5]])}...")
    
    # 3. Get specific breach
    print("\n3. Get details for specific breach:")
    try:
        adobe = hibp.get_breach("Adobe")
        print(f"   Name: {adobe.name}")
        print(f"   Domain: {adobe.domain}")
        print(f"   Breach Date: {adobe.breach_date}")
        print(f"   Accounts: {adobe.pwn_count:,}")
        print(f"   Verified: {adobe.is_verified}")
        print(f"   Data Classes: {', '.join(adobe.data_classes[:5])}...")
    except NotFoundError:
        print("   Breach not found")
    
    # 4. Get latest breach
    print("\n4. Get most recent breach:")
    try:
        latest = hibp.get_latest_breach()
        print(f"   Name: {latest.name}")
        print(f"   Added: {latest.added_date}")
    except Exception as e:
        print(f"   Error: {e}")
    
    # 5. Get data classes
    print("\n5. Get all data classes:")
    data_classes = hibp.get_data_classes()
    print(f"   Total: {len(data_classes)}")
    print(f"   Examples: {', '.join(data_classes[:5])}...")
    
    # 6. Filter breaches
    print("\n6. Filter breaches by domain:")
    adobe_breaches = hibp.get_all_breaches(domain="adobe.com")
    print(f"   Adobe breaches: {len(adobe_breaches)}")
    
    # 7. Get spam lists
    print("\n7. Get spam list breaches:")
    spam_lists = hibp.get_all_breaches(is_spam_list=True)
    print(f"   Spam list breaches: {len(spam_lists)}")


def demonstrate_passwords_api():
    """Demonstrate Pwned Passwords API (no API key needed)."""
    print("\n" + "=" * 70)
    print("PWNED PASSWORDS API (No API Key Required)")
    print("=" * 70)
    
    hibp = HIBP()  # No API key needed!
    
    # 1. Check common passwords
    print("\n1. Check common passwords:")
    passwords = [
        "password",
        "123456",
        "qwerty",
        "MyS3cur3P@ssw0rd!2024",
    ]
    
    for pwd in passwords:
        count = hibp.is_password_pwned(pwd)
        if count > 0:
            print(f"   ⚠️  '{pwd}' - Found {count:,} times")
        else:
            print(f"   ✓ '{pwd}' - Not found")
    
    # 2. Use NTLM hash
    print("\n2. Check password using NTLM hash:")
    count = hibp.is_password_pwned("password", use_ntlm=True)
    print(f"   NTLM check: Found {count:,} times")
    
    # 3. Use padding for privacy
    print("\n3. Check password with padding:")
    count = hibp.is_password_pwned("password", add_padding=True)
    print(f"   With padding: Found {count:,} times")
    print("   (Padding makes response size uniform for privacy)")
    
    # 4. Search by hash prefix
    print("\n4. Search by hash prefix (k-Anonymity):")
    results = hibp.search_password_hashes("21BD1")
    print(f"   Found {len(results)} hash suffixes")
    print(f"   Example suffixes: {list(results.keys())[:3]}...")
    
    # 5. Hash utilities
    print("\n5. Hash password utilities:")
    password = "test123"
    sha1_hash = hibp.passwords.hash_password_sha1(password)
    ntlm_hash = hibp.passwords.hash_password_ntlm(password)
    print(f"   Password: {password}")
    print(f"   SHA-1:  {sha1_hash}")
    print(f"   NTLM:   {ntlm_hash}")


def demonstrate_pastes_api():
    """Demonstrate pastes API."""
    print("\n" + "=" * 70)
    print("PASTES API")
    print("=" * 70)
    
    hibp = HIBP(api_key="00000000000000000000000000000000")
    
    print("\nGet pastes for an account:")
    try:
        pastes = hibp.get_account_pastes("account-exists@hibp-integration-tests.com")
        if pastes:
            print(f"   Found {len(pastes)} paste(s)")
            for paste in pastes[:3]:
                print(f"   - Source: {paste.source}")
                print(f"     ID: {paste.id}")
                print(f"     Date: {paste.date}")
                print(f"     Emails: {paste.email_count}")
        else:
            print("   No pastes found")
    except NotFoundError:
        print("   No pastes found")
    except Exception as e:
        print(f"   Error: {e}")


def demonstrate_error_handling():
    """Demonstrate proper error handling."""
    print("\n" + "=" * 70)
    print("ERROR HANDLING")
    print("=" * 70)
    
    hibp = HIBP(api_key="invalid-key-12345678901234567890")
    
    print("\n1. Handling NotFoundError:")
    try:
        breaches = hibp.get_account_breaches("nonexistent@example.com")
        print(f"   Found {len(breaches)} breaches")
    except NotFoundError:
        print("   ✓ Caught NotFoundError - No breaches found")
    except AuthenticationError:
        print("   ✓ Caught AuthenticationError - Invalid API key")
    
    print("\n2. Handling AuthenticationError:")
    try:
        breaches = hibp.get_account_breaches("test@example.com")
    except AuthenticationError as e:
        print(f"   ✓ Caught AuthenticationError: {e}")
    except Exception as e:
        print(f"   Other error: {e}")
    
    print("\n3. Handling RateLimitError:")
    print("   (Would occur if rate limit exceeded)")
    print("   Code: ")
    print("   try:")
    print("       breaches = hibp.get_account_breaches('test@example.com')")
    print("   except RateLimitError as e:")
    print("       print(f'Rate limited. Retry after {e.retry_after}s')")
    print("       time.sleep(e.retry_after)")


def demonstrate_advanced_features():
    """Demonstrate advanced features."""
    print("\n" + "=" * 70)
    print("ADVANCED FEATURES")
    print("=" * 70)
    
    # 1. Custom user agent
    print("\n1. Custom user agent:")
    hibp = HIBP(
        api_key="00000000000000000000000000000000",
        user_agent="MyApp/1.0 (contact@example.com)"
    )
    print("   ✓ Client initialized with custom user agent")
    
    # 2. Custom timeout
    print("\n2. Custom timeout:")
    hibp = HIBP(
        api_key="00000000000000000000000000000000",
        timeout=60
    )
    print("   ✓ Client initialized with 60 second timeout")
    
    # 3. Access individual API modules
    print("\n3. Direct access to API modules:")
    hibp = HIBP(api_key="00000000000000000000000000000000")
    print(f"   Breaches module: {type(hibp.breaches).__name__}")
    print(f"   Passwords module: {type(hibp.passwords).__name__}")
    print(f"   Pastes module: {type(hibp.pastes).__name__}")
    print(f"   Subscription module: {type(hibp.subscription).__name__}")
    print(f"   Stealer logs module: {type(hibp.stealer_logs).__name__}")
    
    # 4. Model to dictionary conversion
    print("\n4. Model conversion:")
    all_breaches = hibp.get_all_breaches()
    if all_breaches:
        breach = all_breaches[0]
        breach_dict = breach.to_dict()
        print(f"   Breach object: {breach}")
        print(f"   As dictionary keys: {list(breach_dict.keys())[:5]}...")


def main():
    """Run all demonstrations."""
    print("=" * 70)
    print("HAVE I BEEN PWNED LIBRARY - COMPLETE DEMONSTRATION")
    print("=" * 70)
    
    demonstrate_breaches_api()
    demonstrate_passwords_api()
    demonstrate_pastes_api()
    demonstrate_error_handling()
    demonstrate_advanced_features()
    
    print("\n" + "=" * 70)
    print("DEMONSTRATION COMPLETE")
    print("=" * 70)
    print("\nKey Takeaways:")
    print("  ✓ All HIBP API v3 endpoints are supported")
    print("  ✓ Pwned Passwords doesn't require an API key")
    print("  ✓ Comprehensive error handling with specific exceptions")
    print("  ✓ Privacy-focused with k-Anonymity for passwords")
    print("  ✓ Easy to use with intuitive method names")
    print("  ✓ Customizable with user agent and timeout options")
    print("  ✓ Well-typed models for all responses")
    print("\nFor more information:")
    print("  - Read README.md for full documentation")
    print("  - Check QUICKSTART.md for quick reference")
    print("  - Visit https://haveibeenpwned.com/API/v3 for API docs")


if __name__ == "__main__":
    main()
