"""
Configuration management for MJ Microstock Prompter
"""
import os
from dotenv import load_dotenv
from typing import Dict, Any

load_dotenv()

class Config:
    """Application configuration class"""
    
    # API Configuration
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    
    # Default Settings
    DEFAULT_PROVIDER = os.getenv("DEFAULT_PROVIDER", "gemini")
    DEFAULT_MODEL = os.getenv("DEFAULT_MODEL", "gemini-2.5-flash")
    MAX_PROMPTS_PER_REQUEST = int(os.getenv("MAX_PROMPTS_PER_REQUEST", "10"))
    DEFAULT_DELAY_SECONDS = int(os.getenv("DEFAULT_DELAY_SECONDS", "3"))
    
    # Model mappings
    PROVIDER_MODELS = {
        "gemini": ["gemini-2.5-flash", "gemini-2.5-flash"],
        "openai": ["gpt-3.5-turbo", "gpt-4", "gpt-4-turbo"]
    }
    
    # Aspect ratio options
    ASPECT_RATIOS = ["16:9", "1:1", "4:3", "9:16", "3:2", "2:3"]
    
    # Default Midjourney parameters
    DEFAULT_MJ_PARAMS = "--q 2 --chaos 50"
    
    @classmethod
    def get_api_key(cls, provider: str) -> str:
        """Get API key for specified provider"""
        if provider.lower() == "gemini":
            return cls.GEMINI_API_KEY
        elif provider.lower() == "openai":
            return cls.OPENAI_API_KEY
        else:
            raise ValueError(f"Unknown provider: {provider}")
    
    @classmethod
    def get_models_for_provider(cls, provider: str) -> list:
        """Get available models for specified provider"""
        return cls.PROVIDER_MODELS.get(provider.lower(), [])
    
    @classmethod
    def validate_config(cls) -> Dict[str, Any]:
        """Validate configuration and return status"""
        issues = []
        
        if not cls.GEMINI_API_KEY:
            issues.append("GEMINI_API_KEY not set")
        
        if not cls.OPENAI_API_KEY:
            issues.append("OPENAI_API_KEY not set")
            
        if cls.DEFAULT_PROVIDER not in cls.PROVIDER_MODELS:
            issues.append(f"Invalid DEFAULT_PROVIDER: {cls.DEFAULT_PROVIDER}")
        
        return {
            "valid": len(issues) == 0,
            "issues": issues,
            "has_gemini": bool(cls.GEMINI_API_KEY),
            "has_openai": bool(cls.OPENAI_API_KEY)
        }

# Global config instance
config = Config()