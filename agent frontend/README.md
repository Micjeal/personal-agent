# Agent Micheal Dashboard

Simple web dashboard to monitor message activity across all channels.

## Features

- **Real-time channel status** - See which channels are online/offline
- **Message monitoring** - View recent messages from all channels
- **Clean interface** - Simple, responsive design
- **Auto-refresh** - Updates every 5 seconds

## Quick Start

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Start the dashboard**:
   ```bash
   python app.py
   ```
   Or double-click `start.bat`

3. **Open browser**: http://127.0.0.1:5000

## Channel Status

- 🟢 **Online** - Channel is active and receiving messages
- 🔴 **Offline** - Channel not configured or disconnected
- 🟡 **Stub** - Implementation placeholder

## Message Display

The dashboard shows:
- Channel type (Email, Telegram, WhatsApp, etc.)
- Message preview (first 100 characters)
- Timestamp (relative time)

## API Endpoints

- `GET /api/status` - Channel connection status
- `GET /api/messages` - Recent messages (last 10)

## Configuration

The dashboard automatically reads messages from:
`../agent micheal/agent_micheal/messages.json`

Make sure the main Agent Micheal is running to see live data.