"""Telegram connector using python-telegram-bot."""
import logging
from datetime import datetime
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes
from ..config import config
from ..core.persistence import Message
from ..utils.security import SecurityUtils
from ..utils.rate_limiter import RateLimiter

logger = logging.getLogger(__name__)

class TelegramConnector:
    """Telegram bot connector."""
    
    def __init__(self, router=None):
        self.router = router
        self.app = None
        self.rate_limiter = RateLimiter(max_requests=config.rate_limit_per_minute)
    
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle incoming Telegram messages."""
        try:
            user_id = str(update.effective_user.id)
            
            # Rate limiting
            if not self.rate_limiter.is_allowed(user_id):
                await update.message.reply_text("Please slow down. You're sending messages too quickly.")
                return
            
            # Create normalized message
            message = Message(
                id=SecurityUtils.generate_message_id(),
                channel='telegram',
                sender_id=user_id,
                sender_name=update.effective_user.full_name or 'Unknown',
                text=SecurityUtils.sanitize_text(update.message.text or ''),
                received_at=datetime.now(),
                metadata={
                    'chat_id': update.effective_chat.id,
                    'message_id': update.message.message_id
                }
            )
            
            # Route message
            if self.router:
                await self.router.route_message(message)
        
        except Exception as e:
            logger.error(f"Error handling Telegram message: {e}")
            await update.message.reply_text("Sorry, I encountered an error processing your message.")
    
    async def send_message(self, chat_id: str, text: str):
        """Send message via Telegram."""
        try:
            await self.app.bot.send_message(chat_id=int(chat_id), text=text)
            logger.info(f"Telegram message sent to {chat_id}")
        except Exception as e:
            logger.error(f"Error sending Telegram message: {e}")
    
    async def start(self):
        """Start the Telegram bot."""
        if not config.telegram_bot_token:
            logger.warning("Telegram bot token not configured")
            return
        
        self.app = Application.builder().token(config.telegram_bot_token).build()
        
        # Add message handler
        message_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message)
        self.app.add_handler(message_handler)
        
        logger.info("Telegram connector started")
        await self.app.run_polling()
    
    def stop(self):
        """Stop the Telegram bot."""
        if self.app:
            self.app.stop_running()