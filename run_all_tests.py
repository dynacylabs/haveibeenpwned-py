#!/usr/bin/env python3
"""
Test runner script that can work even with terminal issues.
This script imports and runs all tests programmatically.
"""

import sys
import os
import subprocess

# Ensure the package is importable
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def check_dependencies():
    """Check if test dependencies are installed."""
    missing = []
    try:
        import pytest
    except ImportError:
        missing.append("pytest")
    
    try:
        import pytest_cov
    except ImportError:
        missing.append("pytest-cov")
    
    try:
        import responses
    except ImportError:
        missing.append("responses")
    
    try:
        import pytest_mock
    except ImportError:
        missing.append("pytest-mock")
    
    return missing

def install_dependencies():
    """Try to install missing dependencies."""
    print("Installing test dependencies...")
    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", 
            "pytest>=7.0.0", "pytest-cov>=4.0.0", 
            "pytest-mock>=3.10.0", "responses>=0.22.0"
        ])
        return True
    except Exception as e:
        print(f"Failed to install dependencies: {e}")
        return False

def run_tests(mode="all"):
    """Run tests using pytest programmatically."""
    import pytest
    
    args = ["-v", "--tb=short"]
    
    if mode == "unit":
        args.extend(["-m", "unit"])
        print("\n" + "="*70)
        print("RUNNING UNIT TESTS (MOCKED)")
        print("="*70 + "\n")
    elif mode == "integration":
        args.extend(["-m", "integration"])
        print("\n" + "="*70)
        print("RUNNING INTEGRATION TESTS (LIVE API)")
        print("="*70 + "\n")
    elif mode == "coverage":
        args.extend([
            "--cov=haveibeenpwned",
            "--cov-report=html",
            "--cov-report=term-missing",
            "--cov-report=xml"
        ])
        print("\n" + "="*70)
        print("RUNNING ALL TESTS WITH COVERAGE")
        print("="*70 + "\n")
    else:
        print("\n" + "="*70)
        print("RUNNING ALL TESTS")
        print("="*70 + "\n")
    
    # Add test directory
    args.append("tests/")
    
    # Run pytest
    exit_code = pytest.main(args)
    
    if mode == "coverage" and exit_code == 0:
        print("\n" + "="*70)
        print("Coverage report generated in htmlcov/index.html")
        print("="*70 + "\n")
    
    return exit_code

def main():
    """Main entry point."""
    # Check dependencies
    missing = check_dependencies()
    
    if missing:
        print(f"Missing dependencies: {', '.join(missing)}")
        print("Attempting to install...")
        if not install_dependencies():
            print("\nPlease install manually:")
            print(f"  pip install {' '.join(missing)}")
            return 1
        
        # Re-check
        missing = check_dependencies()
        if missing:
            print(f"Still missing: {', '.join(missing)}")
            return 1
    
    print("All dependencies installed ✓\n")
    
    # Get mode from command line
    mode = sys.argv[1] if len(sys.argv) > 1 else "all"
    
    if mode not in ["unit", "integration", "coverage", "all"]:
        print(f"Unknown mode: {mode}")
        print("Usage: python run_all_tests.py [unit|integration|coverage|all]")
        return 1
    
    # Run tests
    exit_code = run_tests(mode)
    
    if exit_code == 0:
        print("\n✓ All tests passed!")
    else:
        print(f"\n✗ Tests failed with exit code {exit_code}")
    
    return exit_code

if __name__ == "__main__":
    sys.exit(main())
