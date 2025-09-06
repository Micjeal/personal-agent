"""Natural Language Processing for intent detection."""
import re
from typing import Dict, Any

class IntentDetector:
    """Rule-based intent detection."""
    
    def __init__(self):
        self.intent_patterns = {
            'greeting': [r'\b(hello|hi|hey|good morning|good afternoon)\b'],
            'question': [r'\?', r'\b(what|how|when|where|why|who)\b'],
            'request': [r'\b(please|can you|could you|would you)\b'],
            'complaint': [r'\b(problem|issue|error|bug|wrong)\b'],
            'thanks': [r'\b(thank|thanks|appreciate)\b'],
            'goodbye': [r'\b(bye|goodbye|see you|farewell)\b']
        }
    
    def detect_intent(self, text: str) -> Dict[str, Any]:
        """Detect intent from message text."""
        text_lower = text.lower()
        detected_intents = []
        
        for intent, patterns in self.intent_patterns.items():
            for pattern in patterns:
                if re.search(pattern, text_lower):
                    detected_intents.append(intent)
                    break
        
        return {
            'primary_intent': detected_intents[0] if detected_intents else 'unknown',
            'all_intents': detected_intents,
            'confidence': 0.8 if detected_intents else 0.1
        }
    
    def extract_entities(self, text: str) -> Dict[str, Any]:
        """Extract basic entities from text."""
        entities = {}
        
        # Extract emails
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_pattern, text)
        if emails:
            entities['emails'] = emails
        
        # Extract phone numbers (basic pattern)
        phone_pattern = r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b'
        phones = re.findall(phone_pattern, text)
        if phones:
            entities['phones'] = phones
        
        return entities