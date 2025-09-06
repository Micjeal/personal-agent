"""Email connector using IMAP and SMTP."""
import asyncio
import logging
import smtplib
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from imapclient import IMAPClient
from ..config import config
from ..core.persistence import Message
from ..utils.security import SecurityUtils
from ..utils.retry import retry_async

logger = logging.getLogger(__name__)

class EmailConnector:
    """Email connector for receiving and sending emails."""
    
    def __init__(self, router=None):
        self.router = router
        self.running = False
    
    @retry_async(max_attempts=3)
    async def check_emails(self):
        """Check for new emails via IMAP."""
        try:
            with IMAPClient(config.email_imap_host, port=config.email_imap_port, ssl=True) as client:
                client.login(config.email_user, config.email_password)
                client.select_folder('INBOX')
                
                # Search for unseen messages
                messages = client.search('UNSEEN')
                
                for msg_id in messages:
                    response = client.fetch([msg_id], ['ENVELOPE', 'BODY[TEXT]'])
                    envelope = response[msg_id][b'ENVELOPE']
                    body = response[msg_id][b'BODY[TEXT]'].decode('utf-8', errors='ignore')
                    
                    # Create normalized message
                    message = Message(
                        id=SecurityUtils.generate_message_id(),
                        channel='email',
                        sender_id=envelope.from_[0].mailbox.decode() + '@' + envelope.from_[0].host.decode(),
                        sender_name=envelope.from_[0].name.decode() if envelope.from_[0].name else 'Unknown',
                        text=SecurityUtils.sanitize_text(body),
                        received_at=datetime.now(),
                        metadata={'subject': envelope.subject.decode() if envelope.subject else ''}
                    )
                    
                    # Route message
                    if self.router:
                        await self.router.route_message(message)
                    
                    # Mark as seen
                    client.add_flags([msg_id], ['\\Seen'])
        
        except Exception as e:
            logger.error(f"Error checking emails: {e}")
    
    @retry_async(max_attempts=3)
    async def send_message(self, recipient: str, text: str, subject: str = "Auto Reply"):
        """Send email response."""
        try:
            msg = MIMEMultipart()
            msg['From'] = config.email_user
            msg['To'] = recipient
            msg['Subject'] = subject
            
            msg.attach(MIMEText(text, 'plain'))
            
            with smtplib.SMTP(config.email_smtp_host, config.email_smtp_port) as server:
                server.starttls()
                server.login(config.email_user, config.email_password)
                server.send_message(msg)
            
            logger.info(f"Email sent to {recipient}")
        
        except Exception as e:
            logger.error(f"Error sending email: {e}")
    
    async def start(self):
        """Start the email connector."""
        self.running = True
        logger.info("Email connector started")
        
        while self.running:
            await self.check_emails()
            await asyncio.sleep(30)  # Check every 30 seconds
    
    def stop(self):
        """Stop the email connector."""
        self.running = False