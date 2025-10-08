"""
Authentication utilities for the Universal Ads SDK.
"""

import base64
import hashlib
import time
from typing import Dict, Any
from urllib.parse import urlparse

from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec, utils


class Authenticator:
    """Handles request authentication and signing for the Universal Ads API."""

    def __init__(self, api_key: str, private_key_pem: str):
        """
        Initialize the authenticator.

        Args:
            api_key: The API key for authentication
            private_key_pem: The private key in PEM format for signing requests
        """
        self.api_key = api_key
        self.private_key_pem = private_key_pem

        # Load the private key
        try:
            self.private_key = serialization.load_pem_private_key(
                private_key_pem.encode("utf-8"),
                password=None,
            )
        except Exception as e:
            raise ValueError(f"Invalid private key format: {e}")

    def create_canonical_request(
        self,
        method: str,
        url: str,
        headers: Dict[str, str],
        timestamp: str,
        body: str = "",
    ) -> str:
        """
        Create a canonical request string for signing.

        Args:
            method: HTTP method (GET, POST, PUT, etc.)
            url: Full URL of the request
            headers: Request headers
            timestamp: Unix timestamp as string
            body: Request body (empty for GET requests)

        Returns:
            Canonical request string
        """
        parsed_url = urlparse(url)
        path = parsed_url.path or "/"
        query = parsed_url.query or ""

        canonical_headers = f"x-api-key:{headers['x-api-key']}\nx-timestamp:{timestamp}"
        signed_headers = "x-api-key;x-timestamp"
        body = body if body else ""

        # Match the backend format exactly - method should NOT be uppercase
        canonical_request = (
            f"{method}\n{path}\n{query}\n{canonical_headers}\n{body}\n{signed_headers}"
        )
        return canonical_request

    def sign_request(self, canonical_request: str) -> str:
        """
        Sign the canonical request using ECDSA.

        Args:
            canonical_request: The canonical request string

        Returns:
            Base64-encoded signature
        """
        # Hash the canonical request with SHA-256
        hashed = hashlib.sha256(canonical_request.encode("utf-8")).digest()

        # Sign the digest using ECDSA with Prehashed SHA-256
        signature = self.private_key.sign(
            hashed, ec.ECDSA(utils.Prehashed(hashes.SHA256()))
        )

        # Base64 encode the DER-encoded signature
        return base64.b64encode(signature).decode("utf-8")

    def get_auth_headers(self, method: str, url: str, body: str = "") -> Dict[str, str]:
        """
        Generate authentication headers for a request.

        Args:
            method: HTTP method
            url: Request URL
            body: Request body

        Returns:
            Dictionary of authentication headers
        """
        timestamp = str(int(time.time()))

        headers = {
            "x-api-key": self.api_key,
            "x-timestamp": timestamp,
            "x-sdk-version": "1.0.0",  # SDK identification flag
            "x-sdk-source": "universal-ads-python-sdk",  # SDK identification flag
        }

        # Create canonical request
        canonical_request = self.create_canonical_request(
            method, url, headers, timestamp, body
        )

        # Sign the request
        signature = self.sign_request(canonical_request)
        headers["x-signature"] = signature

        return headers
