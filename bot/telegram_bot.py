import os
import asyncio
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from .question_generator import generate_question

logger = logging.getLogger(__name__)

async def send_daily_quiz(context: ContextTypes.DEFAULT_TYPE):
    """Generates a poll and sends it to the configured channel."""
    channel_id = os.getenv("TELEGRAM_CHANNEL_ID")
    if not channel_id:
        logger.error("TELEGRAM_CHANNEL_ID missing in environment variables.")
        return

    logger.info("Generating daily quiz via AI...")
    question_data = generate_question()
    
    if not question_data:
        logger.error("Failed to generate question data. Sending aborted.")
        return

    try:
        logger.info(f"Targeting channel {channel_id}")
        await context.bot.send_poll(
            chat_id=channel_id,
            question=question_data["question"],
            options=question_data["options"],
            type="quiz",  # Quiz mode enables correct/incorrect tracking
            correct_option_id=question_data["correct_option_id"],
            explanation=question_data.get("explanation", ""),
            is_anonymous=True  # Usually better for channels
        )
        logger.info("Quiz sent successfully!")
    except Exception as e:
        logger.error(f"Error sending poll to channel: {e}", exc_info=True)


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Respond to /start to verify bot works manually."""
    await update.message.reply_text("Hello! I'm the Quiz Bot. I will automatically send puzzles to the configured channel.")

async def trigger_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Manually force a quiz to be sent for testing purposes.
    (Note: In production you might want to restrict this command by user ID)
    """
    await update.message.reply_text("Generating and sending a quiz right now...")
    await send_daily_quiz(context)
