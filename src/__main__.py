"""Main entry point for agent_micheal."""
import asyncio
import logging
import signal
import sys
from .config import config
from .core.router import MessageRouter
from .connectors.email_connector import EmailConnector
from .connectors.telegram_connector import TelegramConnector
from .connectors.whatsapp_connector import WhatsAppConnector
from .connectors.linkedin_connector import LinkedInConnector
from .connectors.instagram_connector import InstagramConnector

# Configure logging
logging.basicConfig(
    level=getattr(logging, config.log_level.upper()),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class AgentMicheal:
    """Main application class."""
    
    def __init__(self):
        self.router = MessageRouter()
        self.connectors = {}
        self.running = False
    
    def setup_connectors(self):
        """Initialize and register all connectors."""
        # Email connector
        if config.email_user and config.email_password:
            email_connector = EmailConnector(self.router)
            self.router.register_connector('email', email_connector)
            self.connectors['email'] = email_connector
            logger.info("Email connector registered")
        
        # Telegram connector
        if config.telegram_bot_token:
            telegram_connector = TelegramConnector(self.router)
            self.router.register_connector('telegram', telegram_connector)
            self.connectors['telegram'] = telegram_connector
            logger.info("Telegram connector registered")
        
        # WhatsApp connector
        if config.twilio_account_sid and config.twilio_auth_token:
            whatsapp_connector = WhatsAppConnector(self.router)
            self.router.register_connector('whatsapp', whatsapp_connector)
            self.connectors['whatsapp'] = whatsapp_connector
            logger.info("WhatsApp connector registered")
        
        # LinkedIn connector (stub)
        linkedin_connector = LinkedInConnector(self.router)
        self.router.register_connector('linkedin', linkedin_connector)
        self.connectors['linkedin'] = linkedin_connector
        logger.info("LinkedIn connector registered (stub)")
        
        # Instagram connector (stub)
        instagram_connector = InstagramConnector(self.router)
        self.router.register_connector('instagram', instagram_connector)
        self.connectors['instagram'] = instagram_connector
        logger.info("Instagram connector registered (stub)")
    
    def setup_signal_handlers(self):
        """Setup signal handlers for graceful shutdown."""
        def signal_handler(signum, frame):
            logger.info(f"Received signal {signum}, shutting down...")
            self.stop()
            sys.exit(0)
        
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
    
    async def start(self):
        """Start the agent."""
        logger.info("Starting Agent Micheal...")
        self.running = True
        
        self.setup_connectors()
        self.setup_signal_handlers()
        
        # Start the router (which starts all connectors)
        await self.router.start()
    
    def stop(self):
        """Stop the agent."""
        logger.info("Stopping Agent Micheal...")
        self.running = False
        self.router.stop()
        
        for connector in self.connectors.values():
            if hasattr(connector, 'stop'):
                connector.stop()

async def main():
    """Main function."""
    agent = AgentMicheal()
    try:
        await agent.start()
    except KeyboardInterrupt:
        logger.info("Received keyboard interrupt")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
    finally:
        agent.stop()

if __name__ == "__main__":
    asyncio.run(main())