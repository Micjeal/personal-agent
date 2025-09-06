"""Security utilities for agent_micheal."""
import hashlib
import hmac
import secrets
from typing import Optional

class SecurityUtils:
    """Security utilities for message validation and encryption."""
    
    @staticmethod
    def generate_message_id() -> str:
        """Generate a secure random message ID."""
        return secrets.token_urlsafe(16)
    
    @staticmethod
    def hash_sender_id(sender_id: str, salt: str = "") -> str:
        """Hash sender ID for privacy."""
        combined = f"{sender_id}{salt}"
        return hashlib.sha256(combined.encode()).hexdigest()[:16]
    
    @staticmethod
    def verify_webhook_signature(payload: bytes, signature: str, secret: str) -> bool:
        """Verify webhook signature for security."""
        expected_signature = hmac.new(
            secret.encode(),
            payload,
            hashlib.sha256
        ).hexdigest()
        return hmac.compare_digest(signature, expected_signature)
    
    @staticmethod
    def sanitize_text(text: str) -> str:
        """Sanitize text input to prevent injection attacks."""
        # Remove potentially dangerous characters
        dangerous_chars = ['<', '>', '"', "'", '&', '\x00']
        sanitized = text
        for char in dangerous_chars:
            sanitized = sanitized.replace(char, '')
        return sanitized.strip()
    
    @staticmethod
    def validate_email(email: str) -> bool:
        """Basic email validation."""
        import re
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))