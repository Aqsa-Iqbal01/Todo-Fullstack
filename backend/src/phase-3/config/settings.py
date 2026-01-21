"""Configuration management for Phase III AI Chatbot"""

import os
from typing import Optional


class Settings:
    """Application settings for the AI chatbot system"""

    def __init__(self):
        # API endpoints
        self.backend_api_url: str = os.getenv(
            "BACKEND_API_URL", "http://localhost:8001/api"
        )

        # Authentication
        self.require_auth: bool = os.getenv("REQUIRE_AUTH", "true").lower() == "true"

        # MCP Configuration
        self.mcp_port: int = int(os.getenv("MCP_PORT", "8080"))
        self.mcp_host: str = os.getenv("MCP_HOST", "localhost")

        # NLP Configuration
        self.intent_threshold: float = float(os.getenv("INTENT_THRESHOLD", "0.7"))
        self.max_input_length: int = int(os.getenv("MAX_INPUT_LENGTH", "500"))

        # API Retry Configuration
        self.api_retry_attempts: int = int(os.getenv("API_RETRY_ATTEMPTS", "3"))
        self.api_retry_delay: float = float(os.getenv("API_RETRY_DELAY", "1.0"))

        # Logging
        self.log_level: str = os.getenv("LOG_LEVEL", "INFO")


# Global settings instance
settings = Settings()