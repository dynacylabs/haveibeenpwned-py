from setuptools import setup, find_packages
import subprocess
import re

def get_version():
    """Get version from git tag or fallback to default."""
    try:
        # Get the latest git tag
        version = subprocess.check_output(
            ["git", "describe", "--tags", "--abbrev=0"],
            stderr=subprocess.DEVNULL,
            text=True
        ).strip()
        # Remove 'v' prefix if present
        version = re.sub(r'^v', '', version)
        return version
    except (subprocess.CalledProcessError, FileNotFoundError):
        # Fallback version if git is not available or no tags exist
        return "0.0.0.dev0"

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="haveibeenpwned-py",
    version=get_version(),
    author="HaveIBeenPwned API Client",
    description="Python client library for the Have I Been Pwned API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dynacylabs/haveibeenpwned",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Security",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.8",
    install_requires=[
        "requests>=2.25.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "pytest-mock>=3.10.0",
            "responses>=0.22.0",
            "coverage>=7.0.0",
            "black>=21.0",
            "flake8>=3.9",
        ],
        "test": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "pytest-mock>=3.10.0",
            "responses>=0.22.0",
            "coverage>=7.0.0",
        ],
    },
)
