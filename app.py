from flask import Flask, render_template, request, redirect, url_for, jsonify
import subprocess
import os
from dotenv import load_dotenv
from speaker_bot import run_speaker_bot

# Load environment variables
load_dotenv()

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        token = request.form.get('token') or os.getenv('NOTION_TOKEN')
        database_id = request.form.get('database_id') or os.getenv('DATABASE_ID')
        
        if not token or not database_id:
            return render_template('index.html', error="Missing Notion token or database ID")

        # Save token & db id in a temp file
        with open("config.txt", "w") as f:
            f.write(f"{token}\n{database_id}")

        try:
            # Run speaker_bot.py as subprocess (avoids pyttsx3 thread error)
            subprocess.Popen(["python3", "speaker_bot.py"])
            # Initialize control state
            with open("control.txt", "w") as f:
                f.write("resume")
            return render_template('index.html', started=True)
        except Exception as e:
            return render_template('index.html', error=f"Failed to start bot: {str(e)}")

    return render_template('index.html')

@app.route('/pause', methods=['POST'])
def pause():
    with open("control.txt", "w") as f:
        f.write("pause")
    return "Bot manually paused."

@app.route('/resume', methods=['POST'])
def resume():
    with open("control.txt", "w") as f:
        f.write("resume")
    return "Bot resumed."

@app.route('/status', methods=['GET'])
def get_status():
    """Get current bot status"""
    try:
        with open("control.txt", "r") as f:
            state = f.read().strip()
            if state == "auto_pause":
                return jsonify({"status": "auto_paused", "message": "Waiting for next team. Click Resume to continue."})
            elif state == "pause":
                return jsonify({"status": "paused", "message": "Bot manually paused."})
            elif state == "resume":
                return jsonify({"status": "running", "message": "Bot is running..."})
            elif state == "completed":
                return jsonify({"status": "completed", "message": "All team updates completed! 🎉"})
            else:
                return jsonify({"status": "unknown", "message": f"Unknown status: {state}"})
    except FileNotFoundError:
        return jsonify({"status": "not_started", "message": "Bot not started yet."})


if __name__ == '__main__':
    app.run(debug=True)
