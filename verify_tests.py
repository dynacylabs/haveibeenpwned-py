#!/usr/bin/env python3
"""
Simple test verification - checks if all test modules are valid.
"""

import sys
import os

# Add the package to path
sys.path.insert(0, '/workspaces/haveibeenpwned')

def test_imports():
    """Test that all modules import correctly."""
    print("Testing imports...")
    
    try:
        import haveibeenpwned
        print("✓ haveibeenpwned package imports")
    except Exception as e:
        print(f"✗ Failed to import haveibeenpwned: {e}")
        return False
    
    try:
        from haveibeenpwned import HIBP
        print("✓ HIBP class imports")
    except Exception as e:
        print(f"✗ Failed to import HIBP: {e}")
        return False
    
    try:
        from haveibeenpwned import Breach, Paste, Subscription, SubscribedDomain
        print("✓ All models import")
    except Exception as e:
        print(f"✗ Failed to import models: {e}")
        return False
    
    try:
        from haveibeenpwned import exceptions
        print("✓ Exceptions module imports")
    except Exception as e:
        print(f"✗ Failed to import exceptions: {e}")
        return False
    
    return True

def test_basic_functionality():
    """Test basic functionality without hitting API."""
    print("\nTesting basic functionality...")
    
    try:
        from haveibeenpwned import HIBP
        
        # Test initialization
        client = HIBP()
        print("✓ Client initializes without API key")
        
        client = HIBP(api_key="test_key")
        print("✓ Client initializes with API key")
        
        # Test model creation
        from haveibeenpwned import Breach
        breach_data = {
            "Name": "Test",
            "Title": "Test Breach",
            "Domain": "test.com",
            "BreachDate": "2020-01-01",
            "AddedDate": "2020-01-02",
            "ModifiedDate": "2020-01-03",
            "PwnCount": 1000,
            "Description": "Test",
            "DataClasses": ["Email", "Password"],
            "IsVerified": True,
            "IsFabricated": False,
            "IsSensitive": False,
            "IsRetired": False,
            "IsSpamList": False,
            "IsMalware": False,
            "LogoPath": "test.png"
        }
        breach = Breach(**breach_data)
        print(f"✓ Breach model created: {breach.name}")
        
        return True
    except Exception as e:
        print(f"✗ Basic functionality test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def check_test_files():
    """Check that all test files exist."""
    print("\nChecking test files...")
    
    test_files = [
        "tests/__init__.py",
        "tests/conftest.py",
        "tests/test_client.py",
        "tests/test_models.py",
        "tests/test_breach.py",
        "tests/test_passwords.py",
        "tests/test_other_endpoints.py",
        "tests/test_api.py"
    ]
    
    all_exist = True
    for test_file in test_files:
        path = f"/workspaces/haveibeenpwned/{test_file}"
        if os.path.exists(path):
            size = os.path.getsize(path)
            print(f"✓ {test_file} ({size} bytes)")
        else:
            print(f"✗ {test_file} missing")
            all_exist = False
    
    return all_exist

def count_test_functions():
    """Count test functions in test files."""
    print("\nCounting test functions...")
    
    import re
    test_files = [
        "tests/test_client.py",
        "tests/test_models.py", 
        "tests/test_breach.py",
        "tests/test_passwords.py",
        "tests/test_other_endpoints.py",
        "tests/test_api.py"
    ]
    
    total_tests = 0
    for test_file in test_files:
        path = f"/workspaces/haveibeenpwned/{test_file}"
        try:
            with open(path, 'r') as f:
                content = f.read()
                # Count test functions
                tests = re.findall(r'^\s*def test_\w+', content, re.MULTILINE)
                test_count = len(tests)
                total_tests += test_count
                print(f"  {test_file}: {test_count} tests")
        except Exception as e:
            print(f"  {test_file}: Error reading ({e})")
    
    print(f"\nTotal test functions: {total_tests}")
    return total_tests

def main():
    print("="*70)
    print("HAVEIBEENPWNED LIBRARY - TEST VERIFICATION")
    print("="*70 + "\n")
    
    # Run all checks
    imports_ok = test_imports()
    functionality_ok = test_basic_functionality()
    files_ok = check_test_files()
    test_count = count_test_functions()
    
    print("\n" + "="*70)
    print("SUMMARY")
    print("="*70)
    print(f"Imports: {'✓ PASS' if imports_ok else '✗ FAIL'}")
    print(f"Basic functionality: {'✓ PASS' if functionality_ok else '✗ FAIL'}")
    print(f"Test files: {'✓ PASS' if files_ok else '✗ FAIL'}")
    print(f"Total test functions: {test_count}")
    
    if imports_ok and functionality_ok and files_ok and test_count > 0:
        print("\n✓ Library is ready for testing!")
        print(f"\nTo run tests:")
        print("  pytest -m unit                    # Unit tests only")
        print("  pytest -m integration             # Integration tests")
        print("  pytest --cov=haveibeenpwned       # With coverage")
        return 0
    else:
        print("\n✗ Some checks failed")
        return 1

if __name__ == "__main__":
    sys.exit(main())
