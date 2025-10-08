"""
Setup script for the Universal Ads SDK.
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [
        line.strip() for line in fh if line.strip() and not line.startswith("#")
    ]

setup(
    name="universal-ads-sdk",
    version="1.0.0",
    author="Universal Ads",
    author_email="support@universalads.com",
    description="Python SDK for the Universal Ads Third Party API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/universal-ads/universal-ads-sdk-python",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov>=2.0",
            "black>=21.0",
            "flake8>=3.8",
            "mypy>=0.800",
        ],
    },
    keywords="ads, advertising, api, sdk, universal-ads",
    project_urls={
        "Bug Reports": "https://github.com/universal-ads/universal-ads-sdk-python/issues",
        "Source": "https://github.com/universal-ads/universal-ads-sdk-python",
        "Documentation": "https://docs.universalads.com/sdk/python",
    },
)
