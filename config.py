"""
Configuration module for DATA HEARTBEAT with type-safe validation.
Uses Pydantic for robust environment variable management.
"""
import os
from typing import Optional
from pydantic_settings import BaseSettings
from pydantic import Field, validator
from dotenv import load_dotenv

load_dotenv()

class DataHeartbeatConfig(BaseSettings):
    """Central configuration with validation and defaults."""
    
    # Firebase Configuration (CRITICAL - Ecosystem requirement)
    FIREBASE_PROJECT_ID: str = Field(..., env="FIREBASE_PROJECT_ID")
    FIREBASE_CREDENTIALS_PATH: str = Field(..., env="FIREBASE_CREDENTIALS_PATH")
    FIREBASE_COLLECTION: str = Field(default="data_heartbeat_vitals")
    
    # Encryption Configuration
    ENCRYPTION_KEY: str = Field(..., env="ENCRYPTION_KEY")
    ENCRYPTION_NONCE_LENGTH: int = Field(default=12)
    ENCRYPTION_TAG_LENGTH: int = Field(default=16)
    
    # Blockchain Configuration
    CONTRACT_ADDRESS: Optional[str] = Field(None, env="CONTRACT_ADDRESS")
    PRIVATE_KEY: Optional[str] = Field(None, env="PRIVATE_KEY")
    RPC_URL: str = Field(default="https://mainnet.base.org")
    CHAIN_ID: int = Field(default=8453)  # Base mainnet
    
    # Auction Configuration
    AUCTION_DURATION_HOURS: int = Field(default=24)
    BID_REVEAL_PERIOD_HOURS: int = Field(default=2)
    MINIMUM_BID_ETH: float = Field(default=0.01)
    
    # Data Collection Configuration
    COLLECTION_INTERVAL_MINUTES: int = Field(default=5)
    DATA_SEGMENT_DURATION_HOURS: int = Field(default=1)
    
    # System Health Thresholds
    RAM_CRITICAL_THRESHOLD: float = Field(default=0.98)  # 98% RAM usage
    RAM_WARNING_THRESHOLD: float = Field(default=0.85)
    ZERO_BALANCE_THRESHOLD: float = Field(default=0.001)  # 0.001 ETH
    
    # Logging Configuration
    LOG_LEVEL: str = Field(default="INFO")
    LOG_FORMAT: str = Field(
        default="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    
    @validator('ENCRYPTION_KEY')
    def validate_encryption_key(cls, v):
        """Ensure encryption key is properly formatted."""
        if len(v.encode()) != 32:
            raise ValueError(
                f"Encryption key must be 32 bytes (got {len(v.encode())} bytes). "
                "Generate with: openssl rand -base64 32"
            )
        return v
    
    @validator('RPC_URL')
    def validate_rpc_url(cls, v):
        """Validate RPC URL format."""
        if not v.startswith(('http://', 'https://')):
            raise ValueError("RPC_URL must start with http:// or https://")
        return v
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True

# Global configuration instance
config = DataHeartbeatConfig()