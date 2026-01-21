"""Authentication Adapter for Phase II Backend Integration

This module handles authentication delegation to the Phase II backend.
"""

import httpx
from typing import Dict, Any
import sys
import os

# Add the phase-3 directory to the path to allow absolute imports
phase3_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
if phase3_dir not in sys.path:
    sys.path.insert(0, phase3_dir)

from config.settings import settings


class AuthAdapter:
    """Adapter for handling authentication with Phase II backend"""

    def __init__(self):
        self.base_url = settings.backend_api_url

    async def validate_token(self, token: str) -> Dict[str, Any]:
        """
        Validate an authentication token with the backend

        Args:
            token: Authentication token to validate

        Returns:
            Validation result from the backend
        """
        url = f"{self.base_url}/auth/validate"
        headers = {
            "Authorization": f"Bearer {token}"
        }

        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(url, headers=headers)

                if response.status_code == 200:
                    return {
                        "valid": True,
                        "user_data": response.json(),
                        "status_code": response.status_code
                    }
                else:
                    return {
                        "valid": False,
                        "error": f"Token validation failed: {response.text}",
                        "status_code": response.status_code
                    }
        except httpx.RequestError as e:
            return {
                "valid": False,
                "error": f"Request error during token validation: {str(e)}",
                "status_code": None
            }

    async def refresh_token(self, refresh_token: str) -> Dict[str, Any]:
        """
        Refresh an authentication token

        Args:
            refresh_token: Refresh token to use

        Returns:
            New token result from the backend
        """
        url = f"{self.base_url}/auth/refresh"
        headers = {
            "Content-Type": "application/json"
        }
        payload = {
            "refresh_token": refresh_token
        }

        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.post(url, json=payload, headers=headers)

                if response.status_code == 200:
                    return {
                        "success": True,
                        "tokens": response.json(),
                        "status_code": response.status_code
                    }
                else:
                    return {
                        "success": False,
                        "error": f"Token refresh failed: {response.text}",
                        "status_code": response.status_code
                    }
        except httpx.RequestError as e:
            return {
                "success": False,
                "error": f"Request error during token refresh: {str(e)}",
                "status_code": None
            }


# Global auth adapter instance
auth_adapter = AuthAdapter()