import os
from dotenv import load_dotenv
from bot.question_generator import generate_question

load_dotenv()
q = generate_question()
print("Generated Question:", q)