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
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def run_speaker_bot(token, database_id, selected_voice="Charon"):
    notion = Client(auth=token)
    
    # Initialize pyttsx3 engine (always available as fallback)
    engine = pyttsx3.init()
    print("📢 pyttsx3 engine initialized")
    
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

    def fetch_and_tell_joke():
        """Fetch and tell a relevant joke using Gemini AI"""
        print("🎭 Preparing to tell a joke...")
        
        # Update progress to show joke section
        update_progress("", "", total_teams, total_teams, "telling_joke")
        
        max_retries = 3
        joke_attempts = 0
        
        while joke_attempts < max_retries:
            joke_attempts += 1
            print(f"🎯 Joke attempt {joke_attempts}/{max_retries}")
            
            try:
                joke = get_joke_from_gemini()
                if joke and is_good_joke(joke):
                    print(f"😄 Great joke found on attempt {joke_attempts}!")
                    speak("And now, let me share a little humor to end our meeting on a positive note.", 
                          style="friendly", voice=selected_voice)
                    time.sleep(0.5)
                    speak(joke, style="friendly", voice=selected_voice)
                    return
                else:
                    print(f"🔄 Joke not satisfactory, trying again...")
                    if joke_attempts < max_retries:
                        time.sleep(1)  # Brief pause before retry
            except Exception as e:
                print(f"⚠️ Error fetching joke (attempt {joke_attempts}): {e}")
                if joke_attempts < max_retries:
                    time.sleep(1)
        
        # Fallback to a pre-written joke if all attempts fail
        print("📝 Using fallback joke...")
        fallback_joke = "Why do programmers prefer dark mode? Because light attracts bugs!"
        speak("And now for a little tech humor to wrap things up.", style="friendly", voice=selected_voice)
        time.sleep(0.5)
        speak(fallback_joke, style="friendly", voice=selected_voice)

    def get_joke_from_gemini():
        """Get a fresh joke from Gemini AI"""
        if not use_gemini:
            return None
            
        try:
            # Craft a prompt for getting relevant, fresh jokes
            joke_prompt = """Generate a single, original, genuinely funny joke that is:
- Related to business, software development, programming, or workplace life
- Clean and appropriate for a professional meeting
- Fresh and not commonly heard
- Short enough to be told in under 30 seconds
- Actually funny (not just a pun)

Please return ONLY the joke text, no explanations or additional commentary."""

            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=joke_prompt
            )
            
            joke = response.text.strip()
            
            # Clean up the response - remove quotes, extra formatting
            joke = joke.strip('"').strip("'").strip()
            
            # Remove common prefixes that Gemini might add
            prefixes_to_remove = [
                "Here's a joke:",
                "Here's one:",
                "How about this:",
                "Try this one:",
                "Here you go:",
                "Joke:"
            ]
            
            for prefix in prefixes_to_remove:
                if joke.lower().startswith(prefix.lower()):
                    joke = joke[len(prefix):].strip()
            
            return joke
            
        except Exception as e:
            print(f"⚠️ Gemini joke generation error: {e}")
            return None

    def is_good_joke(joke):
        """Basic validation to ensure joke quality"""
        if not joke:
            return False
        
        # Check minimum length (too short might not be a real joke)
        if len(joke) < 20:
            return False
        
        # Check maximum length (too long for a quick meeting end)
        if len(joke) > 400:  # Increased slightly for longer jokes
            return False
        
        # Check for some indicators of a proper joke structure
        joke_indicators = [
            "why", "what", "how", "where", "who",  # Question-based jokes
            "walked into", "said to", "replied",    # Story-based jokes
            "difference between", "called",         # Definition jokes
            "manager", "developer", "programmer",   # Professional context
            "code", "bug", "feature", "deploy",     # Tech context
        ]
        
        joke_lower = joke.lower()
        has_joke_structure = any(indicator in joke_lower for indicator in joke_indicators)
        
        # Also accept if it has quotation marks (dialogue) or exclamation marks (punchlines)
        has_dialogue_or_punchline = '"' in joke or "!" in joke or "?" in joke
        
        # Accept jokes with tech/business terms even without traditional structure
        tech_terms = ["sprint", "production", "local", "backend", "frontend", "api", "server"]
        has_tech_context = any(term in joke_lower for term in tech_terms)
        
        return has_joke_structure or has_dialogue_or_punchline or has_tech_context

    speak("Starting ThursdaySpeakloop bot!", style="welcome", voice=selected_voice)
    
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
        speak(f"Team {team}, it's your turn.", style="friendly", voice=selected_voice)
        
        # Brief pause and then call the teammate immediately
        # time.sleep(0.3)  # Minimal pause for natural flow
        
        # Update progress: announcing teammate
        update_progress(team, selected_teammate, i, total_teams, "announcing_teammate")
        speak(f"{selected_teammate}, please give your update.", style="encouraging", voice=selected_voice)
        # time.sleep(3)
        
        # Update progress: team update in progress
        update_progress(team, selected_teammate, i, total_teams, "update_in_progress")

        # Auto-pause after each team (except the last one)
        if i < total_teams:
            # speak(f"Team {team} update complete. Click Resume to continue to the next team.")
            update_progress(team, selected_teammate, i, total_teams, "auto_paused")
            auto_pause_after_team()
        else:
            speak(f"Team {team} update complete.", style="completion", voice=selected_voice)
            update_progress(team, selected_teammate, i, total_teams, "team_completed")

    speak("Thanks everyone for your updates! All teams have presented.", style="completion", voice=selected_voice)
    
    # Add joke section
    fetch_and_tell_joke()
    
    speak("Have a great day everyone!", style="completion", voice=selected_voice)
    
    # Mark bot as completed
    update_progress("", "", total_teams, total_teams, "completed")
    with open("control.txt", "w") as f:
        f.write("completed")

if __name__ == "__main__":
    with open("config.txt", "r") as f:
        lines = f.read().strip().split('\n')
        token = lines[0]
        database_id = lines[1]
        selected_voice = lines[2] if len(lines) > 2 else "Charon"  # Default to Charon
    run_speaker_bot(token, database_id, selected_voice)