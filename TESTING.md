# Testing Guide for Have I Been Pwned Library

This document explains how to run the comprehensive test suite for the `haveibeenpwned` library.

## Test Suite Overview

The test suite includes:

- **Unit Tests (Mocked)**: Test all functionality with mocked HTTP responses
- **Integration Tests (Live)**: Test against the real HIBP API
- **Coverage Reports**: Measure code coverage with detailed HTML reports

### Test Coverage

- ✅ **Client & HTTP**: Request handling, error responses, timeouts
- ✅ **Models**: Breach, Paste, Subscription, SubscribedDomain
- ✅ **Breaches API**: All 7 endpoints with full parameter testing
- ✅ **Pwned Passwords**: SHA-1, NTLM, padding, k-Anonymity
- ✅ **Pastes API**: Account paste retrieval
- ✅ **Stealer Logs API**: Email, website, and domain searches
- ✅ **Subscription API**: Status retrieval
- ✅ **Main Interface**: All convenience methods

## Installation

Install test dependencies:

```bash
pip install -r requirements-test.txt
```

Or install with test extras:

```bash
pip install -e ".[test]"
```

## Running Tests

### Quick Start

```bash
# Run all unit tests (mocked, no API key needed)
./run_tests.sh mock

# Run integration tests (requires HIBP_API_KEY)
export HIBP_API_KEY="your-api-key-here"
./run_tests.sh live

# Run all tests with coverage
./run_tests.sh coverage
```

### Using pytest directly

```bash
# Run all tests
pytest

# Run only unit tests
pytest -m unit

# Run only integration tests
pytest -m integration

# Run with coverage
pytest --cov=haveibeenpwned --cov-report=html

# Run specific test file
pytest tests/test_passwords.py

# Run specific test
pytest tests/test_passwords.py::TestPwnedPasswordsAPILive::test_check_common_password_live

# Run with verbose output
pytest -v

# Run with detailed output on failures
pytest -vv
```

### Test Runner Script

The `run_tests.sh` script provides convenient test modes:

```bash
./run_tests.sh [MODE]
```

**Modes:**

- `mock` or `unit` - Run unit tests with mocked API
- `live` or `integration` - Run integration tests with live API
- `coverage` or `cov` - Run all tests with coverage report
- `quick` - Run quick unit tests only
- `all` - Run all tests (default)
- `help` - Show help message

**Examples:**

```bash
# Unit tests only (fast, no API key needed)
./run_tests.sh mock

# Integration tests (slow, requires API key)
export HIBP_API_KEY="your-key"
./run_tests.sh live

# Full coverage report
./run_tests.sh coverage

# Quick check
./run_tests.sh quick

# Run everything
./run_tests.sh all
```

## Test Markers

Tests are marked with pytest markers:

- `@pytest.mark.unit` - Unit tests with mocked responses
- `@pytest.mark.integration` - Integration tests hitting live API
- `@pytest.mark.slow` - Tests that are slow to run

Filter tests by marker:

```bash
# Only unit tests
pytest -m unit

# Only integration tests
pytest -m integration

# Exclude slow tests
pytest -m "not slow"

# Unit tests that are not slow
pytest -m "unit and not slow"
```

## Environment Variables

### HIBP_API_KEY

Set your HIBP API key for integration tests:

```bash
export HIBP_API_KEY="your-32-char-hex-api-key"
```

For testing, you can use the test API key:

```bash
export HIBP_API_KEY="00000000000000000000000000000000"
```

**Note**: Integration tests will be skipped if `HIBP_API_KEY` is not set or equals the test key.

## Coverage Reports

### Generating Coverage

```bash
# Generate HTML, terminal, and XML reports
pytest --cov=haveibeenpwned --cov-report=html --cov-report=term-missing --cov-report=xml
```

Or use the test runner:

```bash
./run_tests.sh coverage
```

### Viewing Coverage

**HTML Report** (most detailed):

```bash
# Generate and open
pytest --cov=haveibeenpwned --cov-report=html
open htmlcov/index.html  # macOS
xdg-open htmlcov/index.html  # Linux
```

**Terminal Report**:

```bash
pytest --cov=haveibeenpwned --cov-report=term-missing
```

**Coverage File Locations:**

- HTML: `htmlcov/index.html`
- XML: `coverage.xml`
- Data: `.coverage`

### Coverage Goals

Target: **90%+ code coverage**

Current coverage includes:
- All public API methods
- Error handling paths
- Parameter validation
- Response parsing
- Model conversions

## Test Structure

```
tests/
├── __init__.py              # Test package
├── conftest.py              # Fixtures and configuration
├── test_client.py           # HTTP client and error handling
├── test_models.py           # Data models
├── test_breach.py           # Breach API endpoints
├── test_passwords.py        # Pwned Passwords API
├── test_other_endpoints.py  # Pastes, stealer logs, subscription
└── test_api.py              # Main HIBP interface
```

## Test Fixtures

Common fixtures available in `conftest.py`:

- `mock_client` - HIBP client with test API key
- `live_client` - HIBP client with real API key
- `password_client` - HIBP client without API key
- `responses` - HTTP response mocking
- `sample_breach_data` - Sample breach JSON
- `sample_paste_data` - Sample paste JSON
- `sample_subscription_data` - Sample subscription JSON
- And more...

## Writing Tests

### Unit Test Example

```python
import pytest
import responses as responses_lib
from haveibeenpwned import HIBP

@pytest.mark.unit
def test_get_breach(sample_breach_data):
    """Test getting a single breach."""
    hibp = HIBP()
    
    with responses_lib.RequestsMock() as rsps:
        rsps.add(
            responses_lib.GET,
            "https://haveibeenpwned.com/api/v3/breach/Adobe",
            json=sample_breach_data,
            status=200
        )
        
        breach = hibp.get_breach("Adobe")
        assert breach.name == "Adobe"
```

### Integration Test Example

```python
import pytest
from tests.conftest import skip_if_no_api_key

@pytest.mark.integration
@skip_if_no_api_key()
def test_live_breach_check(live_client):
    """Test checking breaches with live API."""
    breaches = live_client.get_all_breaches()
    assert len(breaches) > 0
```

## Continuous Integration

### GitHub Actions Example

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v2
    
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.9'
    
    - name: Install dependencies
      run: |
        pip install -e .
        pip install -r requirements-test.txt
    
    - name: Run unit tests
      run: pytest -m unit --cov=haveibeenpwned
    
    - name: Run integration tests
      env:
        HIBP_API_KEY: ${{ secrets.HIBP_API_KEY }}
      run: pytest -m integration
      if: env.HIBP_API_KEY != ''
    
    - name: Upload coverage
      uses: codecov/codecov-action@v2
```

## Troubleshooting

### Test Failures

**Import Errors:**

```bash
# Install in development mode
pip install -e .
```

**Missing Dependencies:**

```bash
# Install test dependencies
pip install -r requirements-test.txt
```

**API Rate Limiting:**

- Use unit tests (`pytest -m unit`) which don't hit the API
- Wait for rate limit to reset
- Use a higher tier API key

**Integration Test Failures:**

- Check `HIBP_API_KEY` is set correctly
- Verify API key is valid
- Check internet connection
- Some tests require specific subscription levels

### Common Issues

**"No module named 'haveibeenpwned'"**

```bash
pip install -e .
```

**"HIBP_API_KEY not set" warnings**

```bash
export HIBP_API_KEY="your-key"
# Or use test key
export HIBP_API_KEY="00000000000000000000000000000000"
```

**Coverage not showing**

```bash
# Reinstall with coverage
pip install coverage pytest-cov
# Run with coverage flags
pytest --cov=haveibeenpwned --cov-report=html
```

## Best Practices

1. **Run unit tests first** - Fast feedback loop
2. **Use mocked tests for development** - No API key needed
3. **Run integration tests before commits** - Verify live API works
4. **Check coverage regularly** - Aim for 90%+
5. **Use markers to filter tests** - Run relevant tests only
6. **Set up CI/CD** - Automated testing on every commit

## Getting Help

- Check test output for specific errors
- Review test files for examples
- Run individual tests with `-vv` for details
- Check `conftest.py` for available fixtures
- Refer to pytest documentation: https://docs.pytest.org/

## Summary

```bash
# Quick test workflow
pip install -r requirements-test.txt
./run_tests.sh mock           # Fast unit tests
./run_tests.sh coverage        # Full coverage report
open htmlcov/index.html       # View coverage
```

The test suite ensures the library works correctly across all API endpoints with comprehensive coverage of both mocked and live API scenarios.
