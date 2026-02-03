"""Application configuration."""
from pydantic_settings import BaseSettings
from typing import Optional, List


class Settings(BaseSettings):
    """Application settings."""
    
    # App
    app_name: str = "Smart Campaign Designer"
    debug: bool = False
    
    # AWS Bedrock
    aws_region: str = "us-east-1"
    bedrock_model_id: str = "anthropic.claude-3-sonnet-20240229-v1:0"
    
    # AWS Cognito (可选，不配置则不启用认证)
    cognito_region: str = "us-east-1"
    cognito_user_pool_id: Optional[str] = None
    cognito_app_client_id: Optional[str] = None
    
    # Solver
    solver_timeout_seconds: int = 30
    
    # File Upload
    max_file_size_mb: int = 10
    
    # CORS
    cors_origins: List[str] = ["http://localhost:5173", "http://localhost:3000"]
    
    class Config:
        env_file = ".env"


settings = Settings()
