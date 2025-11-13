# Have I Been Pwned Python Library - Quick Reference

## Installation

```bash
pip install -e .
```

## Quick Start

### 1. Import the library

```python
from haveibeenpwned import HIBP
```

### 2. Initialize the client

```python
# For Pwned Passwords (no API key needed)
hibp = HIBP()

# For breach/paste/stealer log APIs (API key required)
hibp = HIBP(api_key="your-api-key-here")
```

### 3. Common Use Cases

#### Check if a password is compromised

```python
count = hibp.is_password_pwned("password123")
if count > 0:
    print(f"Password found {count} times in breaches!")
```

#### Check if an email has been in breaches

```python
breaches = hibp.get_account_breaches("test@example.com")
for breach in breaches:
    print(f"Found in: {breach.name}")
```

#### Get all breaches in the system

```python
all_breaches = hibp.get_all_breaches()
print(f"Total breaches: {len(all_breaches)}")
```

#### Get details about a specific breach

```python
adobe = hibp.get_breach("Adobe")
print(f"Affected accounts: {adobe.pwn_count:,}")
print(f"Data compromised: {', '.join(adobe.data_classes)}")
```

## API Endpoints Coverage

### ✓ Breaches
- `get_account_breaches(account)` - Get all breaches for an account
- `get_all_breaches()` - Get all breaches in the system
- `get_breach(name)` - Get a single breach by name
- `get_latest_breach()` - Get the most recently added breach
- `get_data_classes()` - Get all data classes
- `get_domain_breaches(domain)` - Get breached emails for a domain
- `get_subscribed_domains()` - Get all subscribed domains

### ✓ Pastes
- `get_account_pastes(account)` - Get all pastes for an account

### ✓ Stealer Logs
- `get_stealer_logs_by_email(email)` - Get domains by email
- `get_stealer_logs_by_website(domain)` - Get emails by website domain
- `get_stealer_logs_by_email_domain(domain)` - Get aliases by email domain

### ✓ Subscription
- `get_subscription_status()` - Get subscription details

### ✓ Pwned Passwords
- `is_password_pwned(password)` - Check if password is compromised
- `search_password_hashes(prefix)` - Search by hash prefix

## Running Examples

```bash
# Test the library
python test_library.py

# Basic usage examples
python examples/basic_usage.py

# Password checking examples
python examples/password_checking.py
```

## Error Handling

```python
from haveibeenpwned import (
    HIBP,
    NotFoundError,
    RateLimitError,
    AuthenticationError,
)

try:
    breaches = hibp.get_account_breaches("test@example.com")
except NotFoundError:
    print("No breaches found")
except RateLimitError as e:
    print(f"Rate limited. Retry after {e.retry_after}s")
except AuthenticationError:
    print("Invalid API key")
```

## Testing with Test API Key

Use `00000000000000000000000000000000` as the API key with test accounts:

```python
hibp = HIBP(api_key="00000000000000000000000000000000")

# Test accounts on hibp-integration-tests.com domain
breaches = hibp.get_account_breaches("account-exists@hibp-integration-tests.com")
breaches = hibp.get_account_breaches("spam-list-only@hibp-integration-tests.com")
breaches = hibp.get_account_breaches("stealer-log@hibp-integration-tests.com")
```

## Project Structure

```
haveibeenpwned/
├── haveibeenpwned/          # Main package
│   ├── __init__.py          # Package exports
│   ├── api.py               # Main HIBP interface
│   ├── breach.py            # Breach endpoints
│   ├── client.py            # HTTP client
│   ├── exceptions.py        # Custom exceptions
│   ├── models.py            # Data models
│   ├── passwords.py         # Pwned Passwords API
│   ├── pastes.py            # Pastes endpoints
│   ├── stealer_logs.py      # Stealer logs endpoints
│   └── subscription.py      # Subscription endpoints
├── examples/                # Usage examples
│   ├── basic_usage.py
│   └── password_checking.py
├── setup.py                 # Package setup
├── requirements.txt         # Dependencies
├── README.md                # Full documentation
└── test_library.py          # Simple tests

```

## Advanced Features

### Custom User Agent

```python
hibp = HIBP(
    api_key="your-key",
    user_agent="MyApp/1.0 (contact@example.com)"
)
```

### Custom Timeout

```python
hibp = HIBP(api_key="your-key", timeout=60)
```

### Access Individual API Modules

```python
# Direct access to API modules
breaches = hibp.breaches.get_breaches_for_account("test@example.com")
pastes = hibp.pastes.get_pastes_for_account("test@example.com")
status = hibp.subscription.get_status()
count = hibp.passwords.check_password("password123")
```

### Pwned Passwords with NTLM and Padding

```python
# Use NTLM hash instead of SHA-1
count = hibp.is_password_pwned("password", use_ntlm=True)

# Add padding for enhanced privacy
count = hibp.is_password_pwned("password", add_padding=True)
```

## Need Help?

- Read the full documentation in README.md
- Check the examples/ directory for code samples
- Review the API documentation: https://haveibeenpwned.com/API/v3
- Get an API key: https://haveibeenpwned.com/API/Key
