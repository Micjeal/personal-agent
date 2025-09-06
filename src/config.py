"""Configuration management for agent_micheal."""
import os
from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()

class Config(BaseModel):
    # Telegram
    telegram_bot_token: str = os.getenv("TELEGRAM_BOT_TOKEN", "")
    
    # Email
    email_imap_host: str = os.getenv("EMAIL_IMAP_HOST", "imap.gmail.com")
    email_imap_port: int = int(os.getenv("EMAIL_IMAP_PORT", "993"))
    email_smtp_host: str = os.getenv("EMAIL_SMTP_HOST", "smtp.gmail.com")
    email_smtp_port: int = int(os.getenv("EMAIL_SMTP_PORT", "587"))
    email_user: str = os.getenv("EMAIL_USER", "")
    email_password: str = os.getenv("EMAIL_PASSWORD", "")
    
    # Twilio
    twilio_account_sid: str = os.getenv("TWILIO_ACCOUNT_SID", "")
    twilio_auth_token: str = os.getenv("TWILIO_AUTH_TOKEN", "")
    twilio_whatsapp_number: str = os.getenv("TWILIO_WHATSAPP_NUMBER", "")
    
    # LinkedIn
    linkedin_client_id: str = os.getenv("LINKEDIN_CLIENT_ID", "")
    linkedin_client_secret: str = os.getenv("LINKEDIN_CLIENT_SECRET", "")
    linkedin_access_token: str = os.getenv("LINKEDIN_ACCESS_TOKEN", "")
    
    # Instagram
    instagram_access_token: str = os.getenv("INSTAGRAM_ACCESS_TOKEN", "")
    instagram_app_id: str = os.getenv("INSTAGRAM_APP_ID", "")
    
    # General
    log_level: str = os.getenv("LOG_LEVEL", "INFO")
    rate_limit_per_minute: int = int(os.getenv("RATE_LIMIT_MESSAGES_PER_MINUTE", "10"))

config = Config()