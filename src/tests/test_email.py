"""Tests for email connector."""
import pytest
from unittest.mock import Mock, patch, MagicMock
from ..connectors.email_connector import EmailConnector
from ..config import config

@pytest.fixture
def email_connector():
    """Create an email connector for testing."""
    return EmailConnector()

@pytest.mark.asyncio
async def test_send_message(email_connector):
    """Test sending email message."""
    with patch('smtplib.SMTP') as mock_smtp:
        mock_server = MagicMock()
        mock_smtp.return_value.__enter__.return_value = mock_server
        
        await email_connector.send_message("test@example.com", "Test message")
        
        mock_server.starttls.assert_called_once()
        mock_server.login.assert_called_once()
        mock_server.send_message.assert_called_once()

@pytest.mark.asyncio
async def test_check_emails():
    """Test checking for new emails."""
    email_connector = EmailConnector()
    
    with patch('imapclient.IMAPClient') as mock_imap:
        mock_client = MagicMock()
        mock_imap.return_value.__enter__.return_value = mock_client
        
        # Mock empty inbox
        mock_client.search.return_value = []
        
        await email_connector.check_emails()
        
        mock_client.login.assert_called_once()
        mock_client.select_folder.assert_called_once_with('INBOX')
        mock_client.search.assert_called_once_with('UNSEEN')

@pytest.mark.asyncio
async def test_check_emails_with_messages():
    """Test checking emails when messages are present."""
    email_connector = EmailConnector()
    mock_router = Mock()
    mock_router.route_message = Mock()
    email_connector.router = mock_router
    
    with patch('imapclient.IMAPClient') as mock_imap:
        mock_client = MagicMock()
        mock_imap.return_value.__enter__.return_value = mock_client
        
        # Mock message data
        mock_client.search.return_value = [1]
        mock_envelope = Mock()
        mock_envelope.from_ = [Mock()]
        mock_envelope.from_[0].mailbox = b'test'
        mock_envelope.from_[0].host = b'example.com'
        mock_envelope.from_[0].name = b'Test User'
        mock_envelope.subject = b'Test Subject'
        
        mock_client.fetch.return_value = {
            1: {
                b'ENVELOPE': mock_envelope,
                b'BODY[TEXT]': b'Test message body'
            }
        }
        
        await email_connector.check_emails()
        
        # Verify message was processed
        assert mock_router.route_message.called