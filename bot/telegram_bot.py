import os
import asyncio
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, PollAnswerHandler
from .question_generator import generate_question
from .database import add_score, get_top_users, reset_weekly_scores

logger = logging.getLogger(__name__)

async def send_daily_quiz(context: ContextTypes.DEFAULT_TYPE):
    """Generates a poll and sends it to the configured channel/group."""
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
        logger.info(f"Targeting channel/group {channel_id}")
        message = await context.bot.send_poll(
            chat_id=channel_id,
            question=question_data["question"],
            options=question_data["options"],
            type="quiz",  # Quiz mode enables correct/incorrect tracking
            correct_option_id=question_data["correct_option_id"],
            explanation=question_data.get("explanation", ""),
            is_anonymous=False  # MUST be False to track who answered to build the leaderboard
        )
        # Store the correct answer id in memory to verify user responses later
        context.bot_data[message.poll.id] = question_data["correct_option_id"]
        logger.info("Quiz sent successfully!")
    except Exception as e:
        logger.error(f"Error sending poll: {e}", exc_info=True)


async def handle_poll_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Triggered when a user answers the non-anonymous quiz poll."""
    answer = update.poll_answer
    poll_id = answer.poll_id
    user = answer.user
    
    # Verify if it's the correct answer
    correct_id = context.bot_data.get(poll_id)
    if correct_id is not None and answer.option_ids:
        user_choice = answer.option_ids[0]
        if user_choice == correct_id:
            # They got it right! Add 1 point
            username = user.username or user.first_name or f"User_{user.id}"
            add_score(user.id, username, points=1)
            logger.info(f"Leaderboard updated: 1 point for {username}")


async def announce_weekly_winners(context: ContextTypes.DEFAULT_TYPE):
    """Sends a message every Sunday night with the top 3 users of the week."""
    channel_id = os.getenv("TELEGRAM_CHANNEL_ID")
    if not channel_id:
        return
        
    top_users = get_top_users(limit=3)
    
    # If no one answered this week
    if not top_users:
        await context.bot.send_message(
            chat_id=channel_id, 
            text="Another week has passed, but it seems no one scored points this week! Let's get algorithm-crushing this week! 💻🚀"
        )
        return
        
    text = "🏆 *Weekly Algorithm Champions!* 🏆\n\nAmazing work everyone! Here are our top problem solvers of the week:\n\n"
    medals = ["1️⃣ 🥇", "2️⃣ 🥈", "3️⃣ 🥉"]
    for i, (username, score) in enumerate(top_users):
        user_str = f"@{username}" if not username.startswith("User_") else username
        text += f"{medals[i]} {user_str} - {score} points\n"
        
    text += "\nKeep up the great work! Points have been reset for the new week. Let's see who claims the top spot next Sunday! 🔥"
    
    await context.bot.send_message(chat_id=channel_id, text=text, parse_mode="Markdown")
    
    # Reset scores after announcing
    reset_weekly_scores()
    logger.info("Weekly winners announced and scores reset.")


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
