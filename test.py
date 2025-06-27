import random
import time
import threading
import pyttsx3
from notion_client import Client

# Configuration - Replace with your actual values or use environment variables
NOTION_TOKEN = "your_notion_token_here"
DATABASE_ID = "your_database_id_here"

# Initialize Notion client
notion = Client(auth=NOTION_TOKEN)

# Initialize Text-to-Speech engine
engine = pyttsx3.init()

# Play/Pause control
pause_event = threading.Event()

def speak(text):
    print(f"🗣️ {text}")
    engine.say(text)
    engine.runAndWait()

def fetch_team_data():
    response = notion.databases.query(database_id=DATABASE_ID)
    results = response.get('results', [])
    
    team_data = {}

    for page in results:
        props = page['properties']
        team_name = props['Name']['title'][0]['plain_text'] if props['Name']['title'] else None
        developers = [dev['name'] for dev in props['Developers']['multi_select']]

        if team_name and developers:
            team_data[team_name] = developers

    return team_data

def pause_listener():
    while True:
        cmd = input("").strip().lower()
        if cmd == 'p':
            print("⏸️ Paused. Press 'r' to resume.")
            pause_event.clear()
        elif cmd == 'r':
            print("▶️ Resumed.")
            pause_event.set()

def main():
    speak("Starting ThursdaySpeakloop bot!")

    team_data = fetch_team_data()
    remaining_teams = list(team_data.keys())
    random.shuffle(remaining_teams)  # Shuffle teams randomly

    # Start pause/resume listener in background
    pause_event.set()  # Initially allow to run
    threading.Thread(target=pause_listener, daemon=True).start()

    for team in remaining_teams:
        teammates = team_data[team]
        selected_teammate = random.choice(teammates)

        # Pause if needed
        pause_event.wait()

        speak(f"Team {team}, it's your turn.")
        time.sleep(1)

        # Pause if needed
        pause_event.wait()

        speak(f"{selected_teammate}, please give your update.")
        
        # Simulate time for speaking update
        time.sleep(3)

    speak("Thanks everyone for your updates! Have a great day!")

if __name__ == "__main__":
    main()
