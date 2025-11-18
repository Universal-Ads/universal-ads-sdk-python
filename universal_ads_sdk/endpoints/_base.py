"""
Base class for endpoint modules.
"""

from typing import Callable, Dict, Any, Optional, Union


class BaseEndpoint:
    """
    Base class for all endpoint modules.

    Provides access to the client's request method.
    """

    def __init__(self, make_request: Callable):
        """
        Initialize the endpoint with a reference to the client's request method.

        Args:
            make_request: The client's _make_request method
        """
        self._make_request = make_request
