from flask import Flask
from threading import Thread

app = Flask(__name__)

@app.route('/')
def home():
    return "Vibranium Bot is alive and running!"

def run():
    # Render assigns a port dynamically via the PORT env var, defaulting to 10000
    import os
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run)
    t.start()