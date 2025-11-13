"""
Example demonstrating password checking with the Pwned Passwords API.
"""

import hashlib
from haveibeenpwned import HIBP


def check_password_strength(password: str):
    """
    Check if a password has been compromised and provide feedback.
    
    Args:
        password: The password to check
    """
    # No API key needed for Pwned Passwords
    hibp = HIBP()
    
    print(f"\nChecking password: {'*' * len(password)}")
    print(f"Length: {len(password)} characters")
    
    # Check if password is pwned
    count = hibp.is_password_pwned(password)
    
    if count == 0:
        print("✓ Good news! This password has not been found in any data breaches.")
        print("  However, still consider:")
        print("  - Using a unique password for each account")
        print("  - Using a password manager")
        print("  - Enabling two-factor authentication")
    else:
        print(f"⚠️  WARNING: This password has been seen {count:,} times in data breaches!")
        print(f"  This password is NOT safe to use.")
        print(f"  Please choose a different password.")
        
        if count > 100000:
            print(f"  ⚠️  CRITICAL: This is an extremely common password!")


def demonstrate_k_anonymity():
    """
    Demonstrate how k-Anonymity protects the password being checked.
    """
    password = "password123"
    
    print("\n" + "=" * 60)
    print("Demonstrating k-Anonymity Protection")
    print("=" * 60)
    
    # Hash the password
    password_hash = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    print(f"\nPassword: {password}")
    print(f"Full SHA-1 hash: {password_hash}")
    
    # Split into prefix and suffix
    prefix = password_hash[:5]
    suffix = password_hash[5:]
    
    print(f"\nSent to API: {prefix} (first 5 characters only)")
    print(f"Kept private: {suffix} (remaining characters)")
    
    # Search by prefix
    hibp = HIBP()
    results = hibp.search_password_hashes(prefix)
    
    print(f"\nAPI returned {len(results)} hash suffixes")
    print(f"Your password {'IS' if suffix in results else 'IS NOT'} in the list")
    
    if suffix in results:
        print(f"Found! This password has been seen {results[suffix]:,} times")


def batch_check_passwords():
    """
    Check multiple passwords at once.
    """
    print("\n" + "=" * 60)
    print("Batch Password Checking")
    print("=" * 60)
    
    passwords = [
        "password",
        "123456",
        "qwerty",
        "letmein",
        "admin",
        "monkey",
        "correcthorsebatterystaple",
        "MyC0mpl3xP@ssw0rd!2024",
    ]
    
    hibp = HIBP()
    
    for password in passwords:
        count = hibp.is_password_pwned(password)
        status = "✓ SAFE" if count == 0 else f"⚠️  PWNED ({count:,} times)"
        print(f"{password:30} {status}")


def main():
    """Run all password examples."""
    
    print("=" * 60)
    print("Pwned Passwords API Examples")
    print("=" * 60)
    
    # Example 1: Check individual passwords
    print("\nExample 1: Check individual passwords")
    print("-" * 60)
    check_password_strength("password123")
    check_password_strength("MyS3cur3P@ssw0rd!2024")
    
    # Example 2: Demonstrate k-Anonymity
    demonstrate_k_anonymity()
    
    # Example 3: Batch check
    batch_check_passwords()
    
    # Example 4: Use padding for enhanced privacy
    print("\n" + "=" * 60)
    print("Using Padding for Enhanced Privacy")
    print("=" * 60)
    hibp = HIBP()
    count = hibp.is_password_pwned("password", add_padding=True)
    print(f"Password check with padding: Found {count:,} times")
    print("Note: Padding makes response sizes uniform for better privacy")
    
    print("\n" + "=" * 60)
    print("All examples completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()
