"""Response templates for different intents and channels."""
from typing import Dict, List
import random

class ResponseTemplates:
    """Template-based response generation."""
    
    def __init__(self):
        self.templates = {
            'greeting': [
                "Hello! How can I help you today?",
                "Hi there! What can I do for you?",
                "Hey! I'm here to assist you."
            ],
            'question': [
                "That's a great question! Let me help you with that.",
                "I'd be happy to help answer your question.",
                "Let me look into that for you."
            ],
            'request': [
                "I'll do my best to help you with that request.",
                "Sure, I can help you with that.",
                "Let me assist you with that."
            ],
            'complaint': [
                "I'm sorry to hear about this issue. Let me help resolve it.",
                "I understand your concern. Let's work on fixing this.",
                "Thank you for bringing this to my attention."
            ],
            'thanks': [
                "You're welcome! Happy to help!",
                "Glad I could assist you!",
                "No problem at all!"
            ],
            'goodbye': [
                "Goodbye! Have a great day!",
                "See you later! Take care!",
                "Bye! Feel free to reach out anytime."
            ],
            'unknown': [
                "I'm not sure I understand. Could you please clarify?",
                "Can you provide more details about what you need?",
                "I'd like to help, but I need more information."
            ]
        }
    
    def get_response(self, intent: str, channel: str = None) -> str:
        """Get a response template for the given intent."""
        templates = self.templates.get(intent, self.templates['unknown'])
        response = random.choice(templates)
        
        # Channel-specific modifications
        if channel == 'email':
            response = f"Dear valued customer,\n\n{response}\n\nBest regards,\nAgent Michael"
        elif channel == 'telegram':
            response = f"🤖 {response}"
        
        return response
    
    def get_auto_reply(self, channel: str) -> str:
        """Get an automatic reply message."""
        auto_replies = {
            'email': "Thank you for your email. I've received your message and will respond shortly.",
            'telegram': "🤖 Thanks for your message! I'm processing it now.",
            'whatsapp': "Hi! I've received your message and will get back to you soon.",
            'linkedin': "Thank you for reaching out on LinkedIn. I'll respond to your message shortly.",
            'instagram': "Thanks for your DM! I'll get back to you as soon as possible."
        }
        return auto_replies.get(channel, "Thank you for your message. I'll respond soon.")