import os
import uuid
import asyncio
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import ParseMode
from telegram.ext import Application, CommandHandler, ContextTypes, CallbackQueryHandler
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
        
        quiz_context = question_data.get("context", "").strip()
        if quiz_context:
            await context.bot.send_message(
                chat_id=channel_id,
                text=quiz_context,
                parse_mode=ParseMode.HTML
            )
            
        quiz_id = str(uuid.uuid4())[:8] # Short unique ID for the callback data
        correct_idx = question_data["correct_option_id"]
        
        # Save correct answer, empty dict to track user choices, and explanation
        context.bot_data[f"quiz_{quiz_id}_correct"] = correct_idx
        context.bot_data[f"quiz_{quiz_id}_answered"] = {}  # Changed to dict
        context.bot_data[f"quiz_{quiz_id}_explanation"] = question_data.get("explanation", "That is the correct answer!")

        # Create inline keyboard from the AI options
        labels = ["A", "B", "C", "D"]
        formatted_options = []
        
        button_row_1 = []
        button_row_2 = []

        for i, option in enumerate(question_data["options"]):
            label = labels[i] if i < len(labels) else str(i)
            # Clean up literal "\n" strings from the AI and display them nicely
            cleaned_option = str(option).replace("\\n", "\n   ").replace("`", "")
            
            # Format the text with HTML bold for the label, and put the answer inside <code> block so it has a cool background
            formatted_options.append(f"<b>{label})</b> <code>{cleaned_option}</code>")
            
            # Setup the data that will be sent back when the user taps it (max 64 bytes)
            callback_data = f"q:{quiz_id}:{i}"
            btn = InlineKeyboardButton(text=f"Option {label}", callback_data=callback_data)
            
            # Group buttons 2x2 for a cleaner UI layout
            if i < 2:
                button_row_1.append(btn)
            else:
                button_row_2.append(btn)
                
        reply_markup = InlineKeyboardMarkup([button_row_1, button_row_2])
        
        # Join options with a blank line between them for readability
        options_text = "\n\n".join(formatted_options)

        # Post the question itself with the clickable inline keyboard
        question_text = f"✌️ <b>Daily Challenge</b>\n\n{question_data['question']}\n\n{options_text}\n\n<i>Tap a letter below to answer!</i>"
        
        await context.bot.send_message(
            chat_id=channel_id,
            text=question_text,
            reply_markup=reply_markup,
            parse_mode=ParseMode.HTML
        )
        
        logger.info("Quiz with inline buttons sent successfully!")
    except Exception as e:
        logger.error(f"Error sending inline quiz: {e}", exc_info=True)


async def handle_button_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Triggered when a user clicks an inline button on a quiz message."""
    query = update.callback_query
    user = query.from_user
    
    if not query.data or not query.data.startswith("q:"):
        return
        
    _, quiz_id, chosen_idx_str = query.data.split(":")
    chosen_idx = int(chosen_idx_str)
    
    correct_idx = context.bot_data.get(f"quiz_{quiz_id}_correct")
    answered_users = context.bot_data.get(f"quiz_{quiz_id}_answered")
    
    # Get the explanation and clean up any leftover HTML tags (Telegram pop-ups do not support HTML)
    explanation = context.bot_data.get(f"quiz_{quiz_id}_explanation", "")
    explanation = explanation.replace("<code>", "`").replace("</code>", "`").replace("<b>", "").replace("</b>", "")
    
    # If the bot restarted or the quiz is too old to be in memory
    if correct_idx is None or answered_users is None:
        await query.answer("This quiz has expired or the bot was restarted recently!", show_alert=True)
        return
    
    labels = ["A", "B", "C", "D"]
    correct_label = labels[correct_idx] if correct_idx < len(labels) else str(correct_idx)
        
    # Prevent answering multiple times, but give the correct answer if they try
    if user.id in answered_users:
        alert_text = f"🛑 Already played! (Answer: Option {correct_label})\n\n💡 {explanation}"
        if len(alert_text) > 195:
            alert_text = alert_text[:192] + "..."
        await query.answer(text=alert_text, show_alert=True)
        return
        
    # Record that this user answered, preventing them from answering again
    answered_users[user.id] = chosen_idx
    
    if chosen_idx == correct_idx:
        # They got it right! Update DB!
        username = user.username or user.first_name or f"User_{user.id}"
        add_score(user.id, username, points=1)
        logger.info(f"Leaderboard updated: 1 DB point for {username}")
        
        # 'show_alert=True' pops up a dialog on the user's phone directly
        alert_text = f"🎉 Correct! +1 point!\n\n💡 {explanation}"
        if len(alert_text) > 195:
            alert_text = alert_text[:192] + "..."
        await query.answer(text=alert_text, show_alert=True)
    else:
        # They got it wrong.
        alert_text = f"❌ Incorrect! Keep practicing!\n\n💡 {explanation}"
        if len(alert_text) > 195:
            alert_text = alert_text[:192] + "..."
        await query.answer(text=alert_text, show_alert=True)


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
