#!/usr/bin/env python3
"""
Test Gemini TTS functionality
"""

import os
import time
import tempfile
import wave
import pygame
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

def test_gemini_tts():
    """Test Gemini text-to-speech"""
    print("🧪 Testing Gemini TTS...")
    
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        print("❌ No GEMINI_API_KEY found")
        return False
    
    try:
        client = genai.Client(api_key=api_key)
        
        # Initialize pygame
        pygame.mixer.init(frequency=24000, size=-16, channels=1, buffer=512)
        print("✅ Pygame initialized")
        
        # Test TTS
        text = "Hello, this is a test of Gemini AI text-to-speech."
        voice_name = "Puck"
        
        print(f"🗣️ Generating speech: '{text}'")
        print(f"🎭 Voice: {voice_name}")
        
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
        
        print("✅ Gemini TTS response received")
        
        audio_data = response.candidates[0].content.parts[0].inline_data.data
        print(f"✅ Audio data received ({len(audio_data)} bytes)")
        
        # Save and play audio
        def wave_file(filename, pcm, channels=1, rate=24000, sample_width=2):
            with wave.open(filename, "wb") as wf:
                wf.setnchannels(channels)
                wf.setsampwidth(sample_width)
                wf.setframerate(rate)
                wf.writeframes(pcm)
        
        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_file:
            wave_file(temp_file.name, audio_data)
            print(f"✅ Audio saved to {temp_file.name}")
            
            pygame.mixer.music.load(temp_file.name)
            pygame.mixer.music.play()
            print("🔊 Playing audio...")
            
            # Wait for playback to finish
            while pygame.mixer.music.get_busy():
                time.sleep(0.1)
            
            print("✅ Audio playback completed")
            
            # Clean up temp file
            os.unlink(temp_file.name)
            print("✅ Temp file cleaned up")
        
        return True
        
    except Exception as e:
        print(f"❌ Gemini TTS error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🎤 Gemini TTS Test")
    print("=" * 30)
    
    success = test_gemini_tts()
    
    print("=" * 30)
    if success:
        print("✅ Gemini TTS working correctly!")
    else:
        print("❌ Gemini TTS test failed")
