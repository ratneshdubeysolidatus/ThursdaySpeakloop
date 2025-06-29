import random
import time
import pyttsx3
from notion_client import Client

def run_speaker_bot(token, database_id):
    notion = Client(auth=token)
    engine = pyttsx3.init()

    def speak(text):
        print(f"🗣️ {text}")
        engine.say(text)
        engine.runAndWait()

    def fetch_team_data():
        response = notion.databases.query(database_id=database_id)
        results = response.get('results', [])
        team_data = {}

        for page in results:
            props = page['properties']
            team_name = props['Name']['title'][0]['plain_text'] if props['Name']['title'] else None
            developers = [dev['name'] for dev in props['Developers']['multi_select']]

            if team_name and developers:
                team_data[team_name] = developers

        return team_data

    def wait_if_paused():
        while True:
            try:
                with open("control.txt", "r") as f:
                    state = f.read().strip()
                    if state == "pause":
                        print("⏸️ Paused...")
                        time.sleep(1)
                    else:
                        break
            except FileNotFoundError:
                break

    def auto_pause_after_team():
        """Auto-pause and wait for manual resume"""
        with open("control.txt", "w") as f:
            f.write("auto_pause")
        print("⏸️ Automatically paused. Waiting for manual resume...")
        
        while True:
            try:
                with open("control.txt", "r") as f:
                    state = f.read().strip()
                    if state == "resume":
                        print("▶️ Resumed by user.")
                        break
                    time.sleep(0.5)  # Check more frequently for responsiveness
            except FileNotFoundError:
                time.sleep(0.5)

    speak("Starting ThursdaySpeakloop bot!")

    team_data = fetch_team_data()
    remaining_teams = list(team_data.keys())
    random.shuffle(remaining_teams)
    total_teams = len(remaining_teams)

    for i, team in enumerate(remaining_teams, 1):
        teammates = team_data[team]
        selected_teammate = random.choice(teammates)

        wait_if_paused()
        speak(f"Team {team}, it's your turn.")
        time.sleep(1)

        wait_if_paused()
        speak(f"{selected_teammate}, please give your update.")
        time.sleep(3)

        # Auto-pause after each team (except the last one)
        if i < total_teams:
            speak(f"Team {team} update complete. Click Resume to continue to the next team.")
            auto_pause_after_team()
        else:
            speak(f"Team {team} update complete.")

    speak("Thanks everyone for your updates! All teams have presented. Have a great day!")
    
    # Mark bot as completed
    with open("control.txt", "w") as f:
        f.write("completed")

if __name__ == "__main__":
    with open("config.txt", "r") as f:
        token = f.readline().strip()
        database_id = f.readline().strip()
    run_speaker_bot(token, database_id)