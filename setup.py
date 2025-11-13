from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="haveibeenpwned",
    version="1.0.0",
    author="HaveIBeenPwned API Client",
    description="Python client library for the Have I Been Pwned API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/haveibeenpwned",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Security",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.7",
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
