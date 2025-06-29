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

        # Check if bot is already running
        try:
            with open("control.txt", "r") as f:
                current_state = f.read().strip()
                if current_state not in ["completed", "not_started"]:
                    return render_template('index.html', error="Bot is already running. Please wait for it to complete.")
        except FileNotFoundError:
            pass  # File doesn't exist, it's safe to start

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

@app.route('/progress', methods=['GET'])
def get_progress():
    """Get current progress information"""
    try:
        with open("progress.txt", "r") as f:
            import json
            progress_data = json.loads(f.read())
            return jsonify(progress_data)
    except FileNotFoundError:
        return jsonify({
            "current_team": "",
            "selected_teammate": "",
            "team_number": 0,
            "total_teams": 0,
            "status": "not_started",
            "completed_teams": 0
        })
    except json.JSONDecodeError:
        return jsonify({
            "current_team": "",
            "selected_teammate": "",
            "team_number": 0,
            "total_teams": 0,
            "status": "error",
            "completed_teams": 0
        })

@app.route('/reset', methods=['POST'])
def reset_session():
    """Reset the bot session for a fresh start"""
    try:
        # Clean up control files
        if os.path.exists("control.txt"):
            os.remove("control.txt")
        if os.path.exists("config.txt"):
            os.remove("config.txt")
        if os.path.exists("progress.txt"):
            os.remove("progress.txt")
        return jsonify({"status": "success", "message": "Session reset successfully."})
    except Exception as e:
        return jsonify({"status": "error", "message": f"Failed to reset session: {str(e)}"})


if __name__ == '__main__':
    app.run(debug=True)
