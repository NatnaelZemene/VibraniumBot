import os
import sys
import logging
import datetime
from dotenv import load_dotenv
from telegram.ext import Application, CommandHandler
from bot.telegram_bot import start_command, trigger_command, send_daily_quiz

# Configure logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

def main():
    # 1. Load environment variables
    load_dotenv()

    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token or token == "your_telegram_bot_token_here":
        logger.error("Error: Please set a valid TELEGRAM_BOT_TOKEN in your .env file")
        sys.exit(1)

    channel_id = os.getenv("TELEGRAM_CHANNEL_ID")
    if not channel_id or channel_id == "@your_channel_username_or_id":
        logger.warning("TELEGRAM_CHANNEL_ID seems to be the default. Make sure to set a valid one in .env")

    # 2. Build the Telegram App
    application = Application.builder().token(token).build()

    # 3. Add bot handlers
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("trigger", trigger_command))

    # 4. Schedule the daily job
    # Using UTC by default
    target_time = datetime.time(hour=10, tzinfo=datetime.timezone.utc) # 10:00 AM UTC
    
    job_queue = application.job_queue
    job_queue.run_daily(callback=send_daily_quiz, time=target_time)
    
    logger.info(f"Bot scheduled to broadcast questions at {target_time} UTC")
    logger.info("Bot is polling...")
    
    # 5. Start Polling for commands
    application.run_polling()

if __name__ == "__main__":
    main()
