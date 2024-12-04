import os
from typing import Dict, Any

class Settings:
    """
    Configuration management for the NPO Audit project
    """
    @staticmethod
    def get_config() -> Dict[str, Any]:
        """
        Retrieve configuration settings from environment variables
        
        :return: Dictionary of configuration settings
        """
        return {
            "openai_api_key": os.getenv("OPENAI_API_KEY"),
            "firecrawl_api_key": os.getenv("FIRECRAWL_API_KEY"),
            "local_llm_base_url": os.getenv("LOCAL_LLM_BASE_URL", "http://localhost:1234/v1"),
            "logging_level": os.getenv("LOGGING_LEVEL", "INFO")
        }