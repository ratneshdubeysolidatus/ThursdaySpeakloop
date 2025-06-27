from flask import Flask, render_template, request, redirect, url_for
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
        token = request.form['token']
        database_id = request.form['database_id']

        # Save token & db id in a temp file
        with open("config.txt", "w") as f:
            f.write(f"{token}\n{database_id}")

        # Run speaker_bot.py as subprocess (avoids pyttsx3 thread error)
        subprocess.Popen(["python3", "speaker_bot.py"])

        # return render_template('success.html')

    return render_template('index.html')

@app.route('/pause', methods=['POST'])
def pause():
    with open("control.txt", "w") as f:
        f.write("pause")
    return "Bot paused."

@app.route('/resume', methods=['POST'])
def resume():
    with open("control.txt", "w") as f:
        f.write("resume")
    return "Bot resumed."


if __name__ == '__main__':
    app.run(debug=True)
