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

    speak("Starting ThursdaySpeakloop bot!")

    team_data = fetch_team_data()
    remaining_teams = list(team_data.keys())
    random.shuffle(remaining_teams)

    for team in remaining_teams:
        teammates = team_data[team]
        selected_teammate = random.choice(teammates)

        wait_if_paused()
        speak(f"Team {team}, it's your turn.")
        time.sleep(1)

        wait_if_paused()
        speak(f"{selected_teammate}, please give your update.")
        time.sleep(3)

    speak("Thanks everyone for your updates! Have a great day!")

if __name__ == "__main__":
    with open("config.txt", "r") as f:
        token = f.readline().strip()
        database_id = f.readline().strip()
    run_speaker_bot(token, database_id)