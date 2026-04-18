# ?? VibraniumBot - Daily Algorithm Challenges for the Community

Welcome to **VibraniumBot**! I built this bot specifically to support my Telegram programming community, [Nathy | Vibranium Coder](https://t.me/vibraniumCoder), by giving them an algorithm challenge every single day. Learning algorithms and data structures requires consistency and discipline. To help everyone stay organized, motivated, and mathematically sharp, this bot delivers a brand new, advanced Python algorithm puzzle daily. 

Powered by Google's Gemini 2.5 Flash AI, VibraniumBot not only drops daily brain-teasers but also automatically tracks everyone's correct answers and celebrates our community's top 3 problem solvers on a Weekly Leaderboard every Sunday night. Let's grow mathematically stronger and write better code together!

## ?? Key Features

- **?? AI-Powered Questions:** Uses \google-genai\ to craft unique, highly technical Python quizzes every day (focusing on decorators, closures, time complexity, etc.).
- **?? Custom Inline Buttons:** Completely bypasses Telegram Channel anonymity limits! Users click beautiful interactive buttons (A/B/C/D) that provide immediate custom pop-up feedback (Correct/Wrong) with AI-generated explanations.
- **?? Live Scoring (PostgreSQL):** Tracks every user's correct answers securely in a PostgreSQL Database. Prevents users from answering the same question twice!
- **? Scheduled Drops for EAT:** Automatically sends the daily challenge at **8:00 AM East Africa Time (EAT)** and announces the Weekly Leaderboard every **Sunday at 8:00 PM EAT**.
- **?? 24/7 Free Hosting Ready:** Includes a lightweight Flask \keep_alive\ server designed specifically to bypass Render's free-tier sleep restrictions when paired with a pinging service like UptimeRobot.

## ??? Tech Stack

- **Language:** Python 3.10+
- **APIs:** Telegram Bot API (\python-telegram-bot[job-queue]\), Google Gemini API (\google-genai\)
- **Database:** PostgreSQL (\psycopg2-binary\) via [Neon.tech](https://neon.tech)
- **Web Server:** \Flask\ (for deployment keep-alive pinging)

## ?? Environment Variables (\.env\)

To run this bot, you must create a \.env\ file in the root directory with the following keys:

\\\env
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_from_botfather
TELEGRAM_CHANNEL_ID=@vibraniumCoder  # Your target channel
GEMINI_API_KEY=your_google_studio_gemini_api_key
DATABASE_URL=postgresql://user:password@host/dbname?sslmode=require
\\\

## ?? Local Development / Setup

1. **Clone the repository and enter the directory:**
   \\\ash
   git clone https://github.com/NatnaelZemene/VibraniumBot.git
   cd "vibranium bot"
   \\\

2. **Create a virtual environment and install dependencies:**
   \\\ash
   python -m venv venv
   .\venv\Scripts\activate  # Windows
   pip install -r requirements.txt
   \\\

3. **Run the bot:**
   \\\ash
   python main.py
   \\\
   *The console should read: "Starting web server to stay awake..." and "Bot is polling..."*

## ?? Free Cloud Deployment Guide

This project is optimized for a **100% Free** serverless setup using Render + Neon + UptimeRobot.

1. **Get a Free PostgreSQL Database:** Go to [Neon Database](https://neon.tech), create a free project, and copy the \DATABASE_URL\ connection string. Put this in your \.env\.
2. **Deploy to Render:** 
   - Go to [Render.com](https://render.com) and create a new **Web Service**.
   - Connect this GitHub repository.
   - **Build Command:** \pip install -r requirements.txt\
   - **Start Command:** \python main.py\
   - Add your 4 Environment Variables (\TELEGRAM_BOT_TOKEN\, \TELEGRAM_CHANNEL_ID\, \GEMINI_API_KEY\, \DATABASE_URL\).
   - Click Deploy.
3. **Keep It Awake (The Magic Trick):**
   - When Render finishes deploying, it gives you a \onrender.com\ URL.
   - Go to [UptimeRobot](https://uptimerobot.com/) (free).
   - Create an \HTTP(s)\ monitor pointing to your Render URL.
   - Set the ping interval to **14 minutes**.
   - *Your bot will now run 24/7 forever without sleeping or costing money!*

## ?? Commands

Once running, you can interact with the bot in Telegram:
- \/start\ - Verify the bot is alive.
- \/trigger\ - (Admin/Test) Force the bot to immediately generate and send a quiz right now instead of waiting for the 8:00 AM EAT schedule.
