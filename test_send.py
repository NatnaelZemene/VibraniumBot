import asyncio
import os
from telegram import Bot

async def test():
    bot = Bot(token="8507434298:AAGHrmisoThrzppBV8RezsaiTrKYAufZqKI")
    try:
        await bot.send_poll(
            chat_id="@vibraniumCoder",
            question="Test Question",
            options=["A", "B", "C", "D"],
            type="quiz",
            correct_option_id=0,
            is_anonymous=True
        )
        print("Success!")
    except Exception as e:
        print(f"Error: {e}")

asyncio.run(test())