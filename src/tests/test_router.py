"""Tests for message router."""
import pytest
import asyncio
from datetime import datetime
from unittest.mock import Mock, AsyncMock
from ..core.router import MessageRouter
from ..core.persistence import Message

@pytest.fixture
def sample_message():
    """Create a sample message for testing."""
    return Message(
        id="test-123",
        channel="test",
        sender_id="user123",
        sender_name="Test User",
        text="Hello, this is a test message",
        received_at=datetime.now(),
        metadata={}
    )

@pytest.fixture
def router():
    """Create a message router for testing."""
    return MessageRouter()

@pytest.mark.asyncio
async def test_register_connector(router):
    """Test connector registration."""
    mock_connector = Mock()
    router.register_connector("test", mock_connector)
    
    assert "test" in router.connectors
    assert router.connectors["test"] == mock_connector

@pytest.mark.asyncio
async def test_route_message(router, sample_message):
    """Test message routing."""
    # Create mock connector with send_message method
    mock_connector = Mock()
    mock_connector.send_message = AsyncMock()
    
    # Register connector
    router.register_connector("test", mock_connector)
    
    # Route message
    await router.route_message(sample_message)
    
    # Verify send_message was called
    mock_connector.send_message.assert_called_once()

@pytest.mark.asyncio
async def test_route_message_no_connector(router, sample_message):
    """Test routing message when no connector is registered."""
    # This should not raise an exception
    await router.route_message(sample_message)

@pytest.mark.asyncio
async def test_route_message_error_handling(router, sample_message):
    """Test error handling in message routing."""
    # Create mock connector that raises an exception
    mock_connector = Mock()
    mock_connector.send_message = AsyncMock(side_effect=Exception("Test error"))
    
    # Register connector
    router.register_connector("test", mock_connector)
    
    # This should not raise an exception (error should be caught)
    await router.route_message(sample_message)