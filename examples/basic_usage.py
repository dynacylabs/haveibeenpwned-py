"""
Example usage of the Have I Been Pwned API library.
"""

from haveibeenpwned import HIBP, NotFoundError, RateLimitError


def main():
    """Demonstrate various API calls."""
    
    # Initialize client with test API key
    # Replace with your actual API key for production use
    api_key = "00000000000000000000000000000000"  # Test key
    hibp = HIBP(api_key=api_key)
    
    print("=" * 60)
    print("Have I Been Pwned API Examples")
    print("=" * 60)
    
    # Example 1: Check account breaches
    print("\n1. Checking account breaches...")
    try:
        test_email = "account-exists@hibp-integration-tests.com"
        breaches = hibp.get_account_breaches(test_email)
        print(f"   Found {len(breaches)} breaches for {test_email}")
        for breach in breaches[:3]:  # Show first 3
            print(f"   - {breach.name}")
    except NotFoundError:
        print("   No breaches found")
    except RateLimitError as e:
        print(f"   Rate limited. Retry after {e.retry_after} seconds")
    
    # Example 2: Get all breaches
    print("\n2. Getting all breaches in the system...")
    all_breaches = hibp.get_all_breaches()
    print(f"   Total breaches in database: {len(all_breaches)}")
    
    # Example 3: Get a specific breach
    print("\n3. Getting details for Adobe breach...")
    try:
        adobe = hibp.get_breach("Adobe")
        print(f"   Name: {adobe.name}")
        print(f"   Date: {adobe.breach_date}")
        print(f"   Accounts affected: {adobe.pwn_count:,}")
        print(f"   Data classes: {', '.join(adobe.data_classes[:5])}...")
    except NotFoundError:
        print("   Breach not found")
    
    # Example 4: Get latest breach
    print("\n4. Getting the most recent breach...")
    try:
        latest = hibp.get_latest_breach()
        print(f"   Latest breach: {latest.name}")
        print(f"   Added: {latest.added_date}")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Example 5: Get data classes
    print("\n5. Getting all data classes...")
    data_classes = hibp.get_data_classes()
    print(f"   Total data classes: {len(data_classes)}")
    print(f"   Examples: {', '.join(data_classes[:5])}...")
    
    # Example 6: Check password (no API key needed!)
    print("\n6. Checking if passwords have been pwned...")
    hibp_free = HIBP()  # No API key needed for passwords
    
    test_passwords = ["password", "correcthorsebatterystaple", "MyS3cur3P@ssw0rd!"]
    for password in test_passwords:
        count = hibp_free.is_password_pwned(password)
        if count > 0:
            print(f"   ⚠️  '{password}' found {count:,} times")
        else:
            print(f"   ✓ '{password}' not found in breaches")
    
    # Example 7: Get pastes
    print("\n7. Checking for paste exposures...")
    try:
        test_email = "account-exists@hibp-integration-tests.com"
        pastes = hibp.get_account_pastes(test_email)
        print(f"   Found {len(pastes)} pastes for {test_email}")
        for paste in pastes[:3]:  # Show first 3
            print(f"   - {paste.source}: {paste.id} ({paste.email_count} emails)")
    except NotFoundError:
        print("   No pastes found")
    except Exception as e:
        print(f"   Error: {e}")
    
    print("\n" + "=" * 60)
    print("Examples completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()
