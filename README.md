<h1 align="center">✌️ VibraniumBot</h1>

<p align="center">
  <strong>An AI-powered Telegram Bot serving daily Python Algorithm Challenges!</strong><br>
  Built originally for the <a href="https://t.me/vibraniumCoder">Nathy | Vibranium Coder</a> community.
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue.svg?logo=python" alt="Python">
  <img src="https://img.shields.io/badge/Telegram-Bot%20API-blue.svg?logo=telegram" alt="Telegram">
  <img src="https://img.shields.io/badge/AI-Google%20Gemini-orange.svg?logo=google" alt="Gemini">
  <img src="https://img.shields.io/badge/Database-PostgreSQL-blue.svg?logo=postgresql" alt="PostgreSQL">
</p>

---

## 🌟 About The Project

Learning algorithms and data structures requires consistency. **VibraniumBot** automates this by delivering a brand new, highly-technical Python algorithm puzzle directly to your Telegram Channel every single day. 

Powered by **Google\'s Gemini 2.5 Flash AI**, it doesn\'t just send questions—it evaluates them, tracks correct answers using interactive buttons, and publishes a **Weekly Leaderboard** to highlight the top programmers in your community!

## ✨ Key Features

- **🧠 Endless AI Content:** Generates unique questions on Python decorators, closures, Big O time complexity, lists, trees, and more. No pre-written question banks!
- **🎨 Custom Inline Buttons & Pop-ups:** Bypasses Telegram\'s "Anonymous Channel" limitations. Users tap beautiful A/B/C/D buttons and get immediate feedback (Correct/Wrong + AI Explanation) in a native pop-up alert.
- **🏆 Live Database Scoring:** Connects to a PostgreSQL database (Neon.tech) to securely track points. Stops users from answering the same question twice!
- **⏰ Fully Automated Scheduling:** Set it and forget it! Defaults to sending the daily challenge at **8:00 AM (East Africa Time)** and announces Weekly Winners every **Sunday at 8:00 PM EAT**.
- **⚡️ 24/7 Free Hosting Ready:** Built with a lightweight \Flask\ server attached, allowing it to run continuously on free cloud platforms like Render without going to sleep.

---

## 🚀 How to Clone & Run It Yourself!

Want to bring VibraniumBot to your own Telegram Community? Follow these steps!

### 1️⃣ Prerequisites

You will need accounts on:
1. **Telegram** (Talk to [@BotFather](https://t.me/botfather) to get your \TELEGRAM_BOT_TOKEN\).
2. **Google AI Studio** (Get your free \GEMINI_API_KEY\).
3. **Neon.tech** (Get your free PostgreSQL \DATABASE_URL\).

### 2️⃣ Clone and Setup Locally

Open your terminal and run the following commands sequentially:

\\ash
# 1. Clone the repository
git clone https://github.com/NatnaelZemene/VibraniumBot.git
cd VibraniumBot

# 2. Create a virtual environment
python -m venv venv

# 3. Activate the environment
# On Windows:
.\\venv\\Scripts\\activate
# On Mac/Linux:
source venv/bin/activate

# 4. Install requirements
pip install -r requirements.txt
\
### 3️⃣ Configure Your Environment

Create a file named \.env\ in the main folder and add your secret keys:

\\env
TELEGRAM_BOT_TOKEN=your_bot_token_from_botfather
TELEGRAM_CHANNEL_ID=@your_target_channel_username
GEMINI_API_KEY=your_gemini_api_key
DATABASE_URL=postgresql://user:password@host/dbname?sslmode=require
\
### 4️⃣ Run the Bot!

\\ash
python main.py
\*If everything is configured correctly, your console will print: "Bot is polling..." and the background Flask server will start!*

---

## ☁️ How to Host it for 100% FREE (24/7)

Don\'t want to leave your computer running all day? Deploy it to the cloud for free!

1. **Deploy to Render.com:**
   - Create a new **Web Service**.
   - Connect your GitHub repository.
   - **Build Command:** \pip install -r requirements.txt   - **Start Command:** \python main.py   - Add your 4 Environment Variables (\TELEGRAM_BOT_TOKEN\, \TELEGRAM_CHANNEL_ID\, \GEMINI_API_KEY\, \DATABASE_URL\) in the Render dashboard.
   - Click Deploy!

2. **Keep it Awake Forever (The Magic Trick):**
   - Free Render services go to sleep after 15 minutes of inactivity. Our code has a \Flask\ server running simultaneously to stop this!
   - Copy the web link Render gives you (e.g., \https://your-bot.onrender.com\).
   - Go to [UptimeRobot.com](https://uptimerobot.com/) and create a free account.
   - Add a new "HTTP(s)" monitor pointing to your Render URL.
   - Set it to ping every **14 minutes**. 
   - **Result:** Your bot will stay awake 24/7 forever without costing a single penny!

---

## 🎮 Commands Summary

These can be typed directly into the bot on Telegram:
- \/start\ - Check if the bot is responsive.
- \/trigger\ - *(Admin testing)* Manually triggers the AI to generate and send a quiz instantly, bypassing the daily clock.

---
Contributions, issues, and feature requests are welcome! Let\'s build better coders together. ✌️
