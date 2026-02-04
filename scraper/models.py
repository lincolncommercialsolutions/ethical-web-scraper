"""
Data models for security reports using Pydantic for validation.
"""

from pydantic import BaseModel, HttpUrl
from typing import Optional, Dict, List
from datetime import datetime


class SecurityReport(BaseModel):
    """
    Structured report containing security-relevant information from a webpage.
    """
    url: HttpUrl
    status_code: int
    timestamp: datetime = datetime.now()
    
    # Page metadata
    title: Optional[str] = None
    meta_description: Optional[str] = None
    
    # Security headers
    security_headers: Dict[str, str] = {}
    missing_important_headers: List[str] = []
    
    # Server/tech stack information
    server: Optional[str] = None
    generator: Optional[str] = None  # e.g., "WordPress 6.4"
    powered_by: Optional[str] = None
    
    # Security.txt compliance
    has_security_txt: bool = False
    security_txt_url: Optional[str] = None
    
    # JavaScript framework detection
    js_framework_hints: List[str] = []
    
    # SSL/TLS information
    ssl_verified: bool = True
    ssl_issuer: Optional[str] = None
    
    # Additional findings
    extracted_emails: List[str] = []
    external_links_count: int = 0
    internal_links_count: int = 0
    
    # Error tracking
    error: Optional[str] = None
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
    
    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization."""
        return self.model_dump(mode='json')
    
    def has_critical_missing_headers(self) -> bool:
        """Check if critical security headers are missing."""
        critical = ["Content-Security-Policy", "Strict-Transport-Security", "X-Frame-Options"]
        return any(h in self.missing_important_headers for h in critical)
