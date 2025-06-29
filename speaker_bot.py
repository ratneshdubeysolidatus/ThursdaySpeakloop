import random
import time
import json
import os
import wave
import tempfile
import pygame
import pyttsx3
from notion_client import Client
from google import genai
from google.genai import types

def run_speaker_bot(token, database_id):
    notion = Client(auth=token)
    
    # Initialize Gemini AI client
    gemini_api_key = os.getenv('GEMINI_API_KEY')
    use_gemini = bool(gemini_api_key)
    
    if use_gemini:
        try:
            client = genai.Client(api_key=gemini_api_key)
            print("🤖 Using Gemini AI for enhanced speech generation")
            # Initialize pygame for audio playback
            pygame.mixer.init(frequency=24000, size=-16, channels=1, buffer=512)
        except Exception as e:
            print(f"⚠️ Gemini AI initialization failed: {e}")
            print("📢 Falling back to pyttsx3")
            use_gemini = False
    
    if not use_gemini:
        engine = pyttsx3.init()
        print("📢 Using pyttsx3 for speech generation")

    def wave_file(filename, pcm, channels=1, rate=24000, sample_width=2):
        """Helper function to save audio data to wave file"""
        with wave.open(filename, "wb") as wf:
            wf.setnchannels(channels)
            wf.setsampwidth(sample_width)
            wf.setframerate(rate)
            wf.writeframes(pcm)

    def speak_with_gemini(text, voice_name="Kore", style_prompt=""):
        """Enhanced speech using Gemini AI with personality and style"""
        try:
            # Add style and personality to the speech
            if style_prompt:
                enhanced_prompt = f"{style_prompt}: {text}"
            else:
                # Default friendly meeting facilitator style
                enhanced_prompt = f"Say this in a friendly, professional meeting facilitator tone: {text}"
            
            response = client.models.generate_content(
                model="gemini-2.5-flash-preview-tts",
                contents=enhanced_prompt,
                config=types.GenerateContentConfig(
                    response_modalities=["AUDIO"],
                    speech_config=types.SpeechConfig(
                        voice_config=types.VoiceConfig(
                            prebuilt_voice_config=types.PrebuiltVoiceConfig(
                                voice_name=voice_name,
                            )
                        )
                    ),
                )
            )
            
            audio_data = response.candidates[0].content.parts[0].inline_data.data
            
            # Save to temporary file and play
            with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_file:
                wave_file(temp_file.name, audio_data)
                pygame.mixer.music.load(temp_file.name)
                pygame.mixer.music.play()
                
                # Wait for playback to finish
                while pygame.mixer.music.get_busy():
                    time.sleep(0.1)
                
                # Clean up temp file
                os.unlink(temp_file.name)
                
        except Exception as e:
            print(f"⚠️ Gemini TTS error: {e}")
            print("📢 Falling back to pyttsx3 for this message")
            speak_with_pyttsx3(text)

    def speak_with_pyttsx3(text):
        """Fallback speech using pyttsx3"""
        engine.say(text)
        engine.runAndWait()

    def speak(text, style="friendly", voice="Kore"):
        """Main speech function with enhanced personality"""
        print(f"🗣️ {text}")
        
        if use_gemini:
            # Define different styles for different types of announcements
            style_prompts = {
                "welcome": "Say this in an enthusiastic, welcoming tone",
                "friendly": "Say this in a friendly, professional meeting facilitator tone",
                "encouraging": "Say this in an encouraging, supportive tone",
                "completion": "Say this in a warm, celebratory tone",
                "transition": "Say this in a smooth, transitional tone"
            }
            
            style_prompt = style_prompts.get(style, style_prompts["friendly"])
            speak_with_gemini(text, voice, style_prompt)
        else:
            speak_with_pyttsx3(text)

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

    speak("Starting ThursdaySpeakloop bot!", style="welcome", voice="Puck")
    
    # Initialize progress
    update_progress("", "", 0, 0, "starting")

    team_data = fetch_team_data()
    remaining_teams = list(team_data.keys())
    random.shuffle(remaining_teams)
    total_teams = len(remaining_teams)

    # Voice variety for different teams
    team_voices = ["Kore", "Puck", "Charon", "Leda", "Aoede", "Enceladus"]
    
    for i, team in enumerate(remaining_teams, 1):
        teammates = team_data[team]
        selected_teammate = random.choice(teammates)
        
        # Use different voices for variety
        team_voice = team_voices[i % len(team_voices)]
        
        # Update progress: announcing team
        update_progress(team, "", i, total_teams, "announcing_team")

        wait_if_paused()
        speak(f"Team {team}, it's your turn.", style="friendly", voice=team_voice)
        time.sleep(1)
        
        # Update progress: announcing teammate
        update_progress(team, selected_teammate, i, total_teams, "announcing_teammate")

        wait_if_paused()
        speak(f"{selected_teammate}, please give your update.", style="encouraging", voice=team_voice)
        time.sleep(3)
        
        # Update progress: team update in progress
        update_progress(team, selected_teammate, i, total_teams, "update_in_progress")

        # Auto-pause after each team (except the last one)
        if i < total_teams:
            # speak(f"Team {team} update complete. Click Resume to continue to the next team.")
            update_progress(team, selected_teammate, i, total_teams, "auto_paused")
            auto_pause_after_team()
        else:
            speak(f"Team {team} update complete.", style="completion", voice=team_voice)
            update_progress(team, selected_teammate, i, total_teams, "team_completed")

    speak("Thanks everyone for your updates! All teams have presented. Have a great day!", style="completion", voice="Puck")
    
    # Mark bot as completed
    update_progress("", "", total_teams, total_teams, "completed")
    with open("control.txt", "w") as f:
        f.write("completed")

if __name__ == "__main__":
    with open("config.txt", "r") as f:
        token = f.readline().strip()
        database_id = f.readline().strip()
    run_speaker_bot(token, database_id)