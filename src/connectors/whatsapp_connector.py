"""WhatsApp connector using Twilio API."""
import logging
from datetime import datetime
from twilio.rest import Client
from ..config import config
from ..core.persistence import Message
from ..utils.security import SecurityUtils
from ..utils.retry import retry_async

logger = logging.getLogger(__name__)

class WhatsAppConnector:
    """WhatsApp connector using Twilio."""
    
    def __init__(self, router=None):
        self.router = router
        self.client = None
        self._initialize_client()
    
    def _initialize_client(self):
        """Initialize Twilio client."""
        if config.twilio_account_sid and config.twilio_auth_token:
            self.client = Client(config.twilio_account_sid, config.twilio_auth_token)
        else:
            logger.warning("Twilio credentials not configured")
    
    async def handle_webhook(self, request_data: dict):
        """Handle incoming WhatsApp webhook from Twilio."""
        try:
            # Extract message data from Twilio webhook
            from_number = request_data.get('From', '')
            body = request_data.get('Body', '')
            
            if not from_number or not body:
                return
            
            # Create normalized message
            message = Message(
                id=SecurityUtils.generate_message_id(),
                channel='whatsapp',
                sender_id=from_number,
                sender_name=request_data.get('ProfileName', 'WhatsApp User'),
                text=SecurityUtils.sanitize_text(body),
                received_at=datetime.now(),
                metadata={
                    'message_sid': request_data.get('MessageSid'),
                    'account_sid': request_data.get('AccountSid')
                }
            )
            
            # Route message
            if self.router:
                await self.router.route_message(message)
        
        except Exception as e:
            logger.error(f"Error handling WhatsApp webhook: {e}")
    
    @retry_async(max_attempts=3)
    async def send_message(self, to_number: str, text: str):
        """Send WhatsApp message via Twilio."""
        if not self.client:
            logger.error("Twilio client not initialized")
            return
        
        try:
            message = self.client.messages.create(
                body=text,
                from_=config.twilio_whatsapp_number,
                to=to_number
            )
            logger.info(f"WhatsApp message sent to {to_number}: {message.sid}")
        
        except Exception as e:
            logger.error(f"Error sending WhatsApp message: {e}")
    
    async def start(self):
        """Start WhatsApp connector (webhook-based)."""
        logger.info("WhatsApp connector ready (webhook-based)")
        # Note: This connector relies on webhooks, so no polling loop needed
    
    def stop(self):
        """Stop WhatsApp connector."""
        logger.info("WhatsApp connector stopped")