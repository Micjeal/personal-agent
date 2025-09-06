"""Rate limiting utilities."""
import time
from collections import defaultdict, deque
from typing import Dict

class RateLimiter:
    """Simple rate limiter to prevent spam."""
    
    def __init__(self, max_requests: int = 10, window_seconds: int = 60):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests: Dict[str, deque] = defaultdict(deque)
    
    def is_allowed(self, identifier: str) -> bool:
        """Check if request is allowed for the given identifier."""
        now = time.time()
        user_requests = self.requests[identifier]
        
        # Remove old requests outside the window
        while user_requests and user_requests[0] <= now - self.window_seconds:
            user_requests.popleft()
        
        # Check if under limit
        if len(user_requests) < self.max_requests:
            user_requests.append(now)
            return True
        
        return False
    
    def get_remaining_requests(self, identifier: str) -> int:
        """Get remaining requests for identifier."""
        now = time.time()
        user_requests = self.requests[identifier]
        
        # Remove old requests
        while user_requests and user_requests[0] <= now - self.window_seconds:
            user_requests.popleft()
        
        return max(0, self.max_requests - len(user_requests))
    
    def reset_user(self, identifier: str) -> None:
        """Reset rate limit for a specific user."""
        if identifier in self.requests:
            del self.requests[identifier]