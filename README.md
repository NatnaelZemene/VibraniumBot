# Daily Programming Quiz Telegram Bot

This is a Telegram Bot designed to generate and send a completely fresh programming/tech quiz to a specific channel every day, fully powered by AI (Google Gemini).

## Prerequisites

1.  **Python 3.10+** minimum
2.  **Telegram Bot Token:** Grab one from [BotFather](https://t.me/BotFather) on Telegram.
3.  **Telegram Channel:** Create a channel, add the bot to it **as an Administrator** (so it can send polls). Get the channel username (e.g., `@my_awesome_tech_channel`).
4.  **Google Gemini API Key:** Grab a free key from the [Google AI Studio](https://aistudio.google.com/).

## Installation

1. Create a virtual environment and install the required packages:

```bash
python -m venv venv
.\venv\Scripts\activate  # On Windows
pip install -r requirements.txt
```

2. Duplicate `.env.example` as `.env`, or rename it, and fill out the details:

```env
TELEGRAM_BOT_TOKEN=123456789:ABCDefgh-your-bot-token
TELEGRAM_CHANNEL_ID=@your_channel_username_here
GEMINI_API_KEY=AIzaSy...your_gemini_key
```

## Running the bot

```bash
python main.py
```

## How It Works

1.  **Start:** The bot spins up and listens to telegram chat updates.
2.  **Scheduling:** Using `python-telegram-bot`'s `JobQueue`, the bot triggers a function once per day at `10:00 AM UTC`. You can modify `main.py` timezone and time logic to change this.
3.  **Generation:** When called, the bot asks Gemini (`gemini-1.5-flash`) for a 4-option JSON puzzle with explanations.
4.  **Sending:** The bot reads the JSON, translates it into a native Telegram Poll element, and broadcasts it to your specified Channel.

## Manual Testing

Before waiting to see if tomorrow's test goes off, test it individually:
- Send the `/trigger` command to your bot via Direct Message on Telegram, and watch it generate and push a new quiz to the channel immediately!
