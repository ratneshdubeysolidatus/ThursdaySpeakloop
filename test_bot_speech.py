#!/usr/bin/env python3
"""
Test the bot's speech function directly
"""

import os
import sys
import time
from dotenv import load_dotenv

# Add the current directory to path to import speaker_bot
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

load_dotenv()

def test_bot_speech():
    """Test the bot's speech functionality"""
    print("🧪 Testing Bot Speech Function")
    print("=" * 40)
    
    # Import the necessary parts
    import tempfile
    import wave
    import pygame
    import pyttsx3
    from google import genai
    from google.genai import types
    
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
    
    # Test different scenarios
    print("\n🎤 Testing speech scenarios:")
    
    print("\n1. Welcome message with Puck voice:")
    speak("Starting ThursdaySpeakloop bot!", style="welcome", voice="Puck")
    time.sleep(1)
    
    print("\n2. Team announcement with Charon voice:")
    speak("Team Frontend, it's your turn.", style="friendly", voice="Charon")
    time.sleep(1)
    
    print("\n3. Member call with Leda voice:")
    speak("Alice, please give your update.", style="encouraging", voice="Leda")
    time.sleep(1)
    
    print("\n✅ All speech tests completed!")

if __name__ == "__main__":
    test_bot_speech()
