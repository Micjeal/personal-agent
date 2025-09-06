# Agent Micheal

An intelligent messaging agent that handles conversations across multiple channels: Email, Telegram, WhatsApp (via Twilio), LinkedIn, and Instagram.

## Features

- **Multi-channel support**: Email, Telegram, WhatsApp, LinkedIn, Instagram
- **Intelligent routing**: Automatic message normalization and routing
- **NLP processing**: Basic intent detection and response generation
- **Rate limiting**: Prevents spam and abuse
- **Security**: Input sanitization and secure credential management
- **Extensible**: Easy to add new channels and handlers

## Project Structure

```
agent_micheal/
├── README.md
├── requirements.txt
├── .env.example
├── Dockerfile
├── src/
│   ├── __main__.py          # Main entry point
│   ├── config.py            # Configuration management
│   ├── connectors/          # Channel connectors
│   │   ├── email_connector.py
│   │   ├── telegram_connector.py
│   │   ├── whatsapp_connector.py
│   │   ├── linkedin_connector.py
│   │   └── instagram_connector.py
│   ├── core/                # Core functionality
│   │   ├── router.py        # Message routing
│   │   ├── handlers.py      # Message processing
│   │   ├── nlp.py          # Intent detection
│   │   ├── templates.py     # Response templates
│   │   └── persistence.py   # Data models
│   ├── utils/               # Utilities
│   │   ├── security.py      # Security functions
│   │   ├── rate_limiter.py  # Rate limiting
│   │   └── retry.py         # Retry logic
│   └── tests/               # Unit tests
│       ├── test_router.py
│       └── test_email.py
```

## Setup

### 1. Clone and Install

```bash
git clone <repository-url>
cd agent_micheal
pip install -r requirements.txt
```

### 2. Environment Configuration

Copy `.env.example` to `.env` and configure your credentials:

```bash
cp .env.example .env
```

Edit `.env` with your actual credentials:

- **Telegram**: Create a bot via @BotFather and get the token
- **Email**: Use app passwords for Gmail/Outlook
- **Twilio**: Get credentials from Twilio console
- **LinkedIn**: Set up LinkedIn app and get OAuth tokens
- **Instagram**: Configure Instagram Graph API access

### 3. Run the Agent

```bash
python -m src
```

## Channel Setup

### Email (IMAP/SMTP)
- Configure IMAP/SMTP settings for your email provider
- Use app passwords for enhanced security
- Supports Gmail, Outlook, and other standard providers

### Telegram
- Create a bot via @BotFather
- Get the bot token and add to `.env`
- The bot will automatically respond to messages

### WhatsApp (Twilio)
- Set up Twilio account and WhatsApp sandbox
- Configure webhook URL for incoming messages
- Add Twilio credentials to `.env`

### LinkedIn (Stub)
- Currently a stub implementation
- Requires LinkedIn Marketing API access
- OAuth 2.0 flow needed for production use

### Instagram (Stub)
- Currently a stub implementation
- Requires Instagram Graph API access
- Webhook subscriptions needed for real-time messages

## Usage

### Basic Auto-Reply
The agent automatically detects intent and responds with appropriate templates:

- **Greetings**: "Hello! How can I help you today?"
- **Questions**: "That's a great question! Let me help you with that."
- **Complaints**: "I'm sorry to hear about this issue. Let me help resolve it."

### Extending Functionality

#### Adding New Intents
Edit `src/core/nlp.py` to add new intent patterns:

```python
self.intent_patterns['new_intent'] = [r'pattern1', r'pattern2']
```

#### Adding Response Templates
Edit `src/core/templates.py` to add new responses:

```python
self.templates['new_intent'] = ["Response 1", "Response 2"]
```

#### Adding New Channels
1. Create a new connector in `src/connectors/`
2. Implement `start()`, `stop()`, and `send_message()` methods
3. Register the connector in `src/__main__.py`

## Testing

Run unit tests:

```bash
pytest src/tests/
```

Run with coverage:

```bash
pytest --cov=src src/tests/
```

## Docker Deployment

Build and run with Docker:

```bash
docker build -t agent-micheal .
docker run --env-file .env agent-micheal
```

## Security Considerations

- All credentials are loaded from environment variables
- Input sanitization prevents injection attacks
- Rate limiting prevents spam and abuse
- Message IDs are securely generated
- Webhook signatures should be verified in production

## Rate Limiting

Default limits:
- 10 messages per minute per user
- Configurable via `RATE_LIMIT_MESSAGES_PER_MINUTE`

## Logging

Logs are configured via `LOG_LEVEL` environment variable:
- `DEBUG`: Detailed debugging information
- `INFO`: General information (default)
- `WARNING`: Warning messages only
- `ERROR`: Error messages only

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

## License

MIT License - see LICENSE file for details.

## Support

For issues and questions:
1. Check the logs for error messages
2. Verify environment configuration
3. Test individual connectors
4. Create an issue with detailed information