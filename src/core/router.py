"""Message routing and coordination."""
import asyncio
import logging
from typing import Dict, Any, Callable
from .persistence import Message
from .handlers import MessageHandler

logger = logging.getLogger(__name__)

class MessageRouter:
    """Routes messages between connectors and handlers."""
    
    def __init__(self):
        self.handler = MessageHandler()
        self.connectors: Dict[str, Any] = {}
        self.running = False
    
    def register_connector(self, channel: str, connector: Any):
        """Register a connector for a specific channel."""
        self.connectors[channel] = connector
        logger.info(f"Registered connector for {channel}")
    
    async def route_message(self, message: Message) -> None:
        """Route incoming message to appropriate handler."""
        try:
            # Process message and get response
            response = await self.handler.process_message(message)
            
            if response and message.channel in self.connectors:
                # Send response back through the same channel
                connector = self.connectors[message.channel]
                if hasattr(connector, 'send_message'):
                    await connector.send_message(message.sender_id, response)
                    logger.info(f"Sent response via {message.channel}")
        
        except Exception as e:
            logger.error(f"Error routing message: {e}")
    
    async def start(self):
        """Start the message router."""
        self.running = True
        logger.info("Message router started")
        
        # Start all registered connectors
        tasks = []
        for channel, connector in self.connectors.items():
            if hasattr(connector, 'start'):
                task = asyncio.create_task(connector.start())
                tasks.append(task)
                logger.info(f"Started {channel} connector")
        
        # Wait for all connectors
        if tasks:
            await asyncio.gather(*tasks, return_exceptions=True)
    
    def stop(self):
        """Stop the message router."""
        self.running = False
        logger.info("Message router stopped")