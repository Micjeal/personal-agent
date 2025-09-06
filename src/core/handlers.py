"""Message handlers for processing and generating replies."""
import logging
from typing import Optional
from .persistence import Message, MessageStore
from .nlp import IntentDetector
from .templates import ResponseTemplates

logger = logging.getLogger(__name__)

class MessageHandler:
    """Handles message processing and response generation."""
    
    def __init__(self):
        self.message_store = MessageStore()
        self.intent_detector = IntentDetector()
        self.templates = ResponseTemplates()
    
    async def process_message(self, message: Message) -> Optional[str]:
        """Process incoming message and generate response."""
        try:
            # Save incoming message
            self.message_store.save_message(message)
            logger.info(f"Processed message from {message.sender_name} on {message.channel}")
            
            # Detect intent
            intent_result = self.intent_detector.detect_intent(message.text)
            primary_intent = intent_result['primary_intent']
            
            # Generate response based on intent
            response = self.templates.get_response(primary_intent, message.channel)
            
            logger.info(f"Generated response for intent: {primary_intent}")
            return response
            
        except Exception as e:
            logger.error(f"Error processing message: {e}")
            return "I'm sorry, I encountered an error processing your message. Please try again."
    
    def get_auto_reply(self, channel: str) -> str:
        """Get automatic reply for a channel."""
        return self.templates.get_auto_reply(channel)