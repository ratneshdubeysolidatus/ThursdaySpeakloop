import random
import time
import json
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

    def update_progress(current_team, selected_teammate, team_number, total_teams, status):
        """Update progress information for the web interface"""
        progress_data = {
            "current_team": current_team,
            "selected_teammate": selected_teammate,
            "team_number": team_number,
            "total_teams": total_teams,
            "status": status,
            "completed_teams": team_number - 1 if status != "completed" else total_teams
        }
        
        with open("progress.txt", "w") as f:
            import json
            f.write(json.dumps(progress_data))

    speak("Starting ThursdaySpeakloop bot!")
    
    # Initialize progress
    update_progress("", "", 0, 0, "starting")

    team_data = fetch_team_data()
    remaining_teams = list(team_data.keys())
    random.shuffle(remaining_teams)
    total_teams = len(remaining_teams)

    for i, team in enumerate(remaining_teams, 1):
        teammates = team_data[team]
        selected_teammate = random.choice(teammates)
        
        # Update progress: announcing team
        update_progress(team, "", i, total_teams, "announcing_team")

        wait_if_paused()
        speak(f"Team {team}, it's your turn.")
        time.sleep(1)
        
        # Update progress: announcing teammate
        update_progress(team, selected_teammate, i, total_teams, "announcing_teammate")

        wait_if_paused()
        speak(f"{selected_teammate}, please give your update.")
        time.sleep(3)
        
        # Update progress: team update in progress
        update_progress(team, selected_teammate, i, total_teams, "update_in_progress")

        # Auto-pause after each team (except the last one)
        if i < total_teams:
            # speak(f"Team {team} update complete. Click Resume to continue to the next team.")
            update_progress(team, selected_teammate, i, total_teams, "auto_paused")
            auto_pause_after_team()
        else:
            speak(f"Team {team} update complete.")
            update_progress(team, selected_teammate, i, total_teams, "team_completed")

    speak("Thanks everyone for your updates! All teams have presented. Have a great day!")
    
    # Mark bot as completed
    update_progress("", "", total_teams, total_teams, "completed")
    with open("control.txt", "w") as f:
        f.write("completed")

if __name__ == "__main__":
    with open("config.txt", "r") as f:
        token = f.readline().strip()
        database_id = f.readline().strip()
    run_speaker_bot(token, database_id)