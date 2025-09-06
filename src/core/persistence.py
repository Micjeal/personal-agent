"""Message persistence and data models."""
from datetime import datetime
from typing import List, Dict, Any, Optional
from pydantic import BaseModel
import json
import os

class Message(BaseModel):
    id: str
    channel: str
    sender_id: str
    sender_name: str
    text: str
    attachments: List[str] = []
    received_at: datetime
    metadata: Dict[str, Any] = {}

class MessageStore:
    """Simple file-based message storage."""
    
    def __init__(self, storage_path: str = "messages.json"):
        self.storage_path = storage_path
        self._ensure_storage_exists()
    
    def _ensure_storage_exists(self):
        if not os.path.exists(self.storage_path):
            with open(self.storage_path, 'w') as f:
                json.dump([], f)
    
    def save_message(self, message: Message) -> None:
        """Save a message to storage."""
        messages = self.load_messages()
        messages.append(message.model_dump(mode='json'))
        with open(self.storage_path, 'w') as f:
            json.dump(messages, f, indent=2, default=str)
    
    def load_messages(self) -> List[Dict]:
        """Load all messages from storage."""
        try:
            with open(self.storage_path, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []
    
    def get_messages_by_channel(self, channel: str) -> List[Dict]:
        """Get messages filtered by channel."""
        messages = self.load_messages()
        return [msg for msg in messages if msg.get('channel') == channel]