"""
Configuration management for the Salary Analyzer system.
"""
import os
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

class Config:
    """Configuration class for the Salary Analyzer."""
    
    def __init__(self):
        self._setup_environment()
        self._validate_config()
    
    def _setup_environment(self):
        """Setup environment variables."""
        try:
            from google.colab import userdata
            os.environ["GOOGLE_API_KEY"] = userdata.get('GOOGLE_API_KEY')
            os.environ["GOOGLE_CSE_ID"] = userdata.get('GOOGLE_CSE_ID')
        except ImportError:
            os.environ["GOOGLE_API_KEY"] = "GOOGLE_API_KEY"
            os.environ["GOOGLE_CSE_ID"] = "GOOGLE_CSE_ID"
    
    def _validate_config(self):
        """Validate configuration."""
        if os.environ["GOOGLE_API_KEY"] == "YOUR_GOOGLE_API_KEY":
            logging.warning("⚠️ WARNING: Please replace 'YOUR_GOOGLE_API_KEY' with your actual Google AI API key.")
    
    @property
    def google_api_key(self) -> str:
        return os.environ["GOOGLE_API_KEY"]
    
    @property
    def google_cse_id(self) -> str:
        return os.environ["GOOGLE_CSE_ID"]
    
    @property
    def gemini_model(self) -> str:
        return "gemini-2.5-flash-lite-preview-06-17"
    
    @property
    def gemini_temperature(self) -> float:
        return 0.7

# Global config instance
config = Config()
