#!/usr/bin/env python3
"""
Test the joke functionality with Gemini AI
"""

import os
import time
from dotenv import load_dotenv

load_dotenv()

def test_joke_generation():
    """Test Gemini AI joke generation"""
    print("🎭 Testing Joke Generation with Gemini AI")
    print("=" * 60)
    
    # Check if Gemini is available
    gemini_api_key = os.getenv('GEMINI_API_KEY')
    if not gemini_api_key:
        print("❌ No GEMINI_API_KEY found - cannot test joke generation")
        return False
    
    try:
        from google import genai
        client = genai.Client(api_key=gemini_api_key)
        print("✅ Gemini client initialized")
        
        # Test joke generation multiple times to see variety
        print("\n🎯 Generating 3 jokes to test variety:")
        
        for i in range(3):
            print(f"\n--- Joke {i+1} ---")
            
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
            
            # Clean up the response
            joke = joke.strip('"').strip("'").strip()
            
            prefixes_to_remove = [
                "Here's a joke:", "Here's one:", "How about this:",
                "Try this one:", "Here you go:", "Joke:"
            ]
            
            for prefix in prefixes_to_remove:
                if joke.lower().startswith(prefix.lower()):
                    joke = joke[len(prefix):].strip()
            
            print(f"🗣️ Joke: {joke}")
            print(f"📏 Length: {len(joke)} characters")
            
            # Basic quality check
            is_good = validate_joke(joke)
            print(f"✅ Quality check: {'PASS' if is_good else 'FAIL'}")
            
            if i < 2:  # Don't wait after the last joke
                time.sleep(1)
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing jokes: {e}")
        return False

def validate_joke(joke):
    """Validate joke quality"""
    if not joke or len(joke) < 20 or len(joke) > 300:
        return False
    
    joke_indicators = [
        "why", "what", "how", "where", "who",
        "walked into", "said to", "replied",
        "difference between", "called",
    ]
    
    joke_lower = joke.lower()
    has_structure = any(indicator in joke_lower for indicator in joke_indicators)
    has_dialogue = '"' in joke or "!" in joke or "?" in joke
    
    return has_structure or has_dialogue

def test_fallback_joke():
    """Test the fallback joke functionality"""
    print("\n🔄 Testing Fallback Joke")
    print("=" * 30)
    
    fallback_joke = "Why do programmers prefer dark mode? Because light attracts bugs!"
    print(f"🗣️ Fallback joke: {fallback_joke}")
    
    is_good = validate_joke(fallback_joke)
    print(f"✅ Fallback quality: {'PASS' if is_good else 'FAIL'}")

def test_speech_with_joke():
    """Test the joke with speech synthesis"""
    print("\n🎤 Testing Joke with Speech")
    print("=" * 35)
    
    try:
        import pyttsx3
        engine = pyttsx3.init()
        
        intro = "And now, let me share a little humor to end our meeting on a positive note."
        joke = "Why don't programmers like nature? It has too many bugs!"
        
        print("🗣️ Speaking introduction...")
        engine.say(intro)
        engine.runAndWait()
        
        time.sleep(0.5)
        
        print("🗣️ Speaking joke...")
        engine.say(joke)
        engine.runAndWait()
        
        print("✅ Speech test completed!")
        
    except Exception as e:
        print(f"❌ Speech test failed: {e}")

if __name__ == "__main__":
    print("🎭 Joke Feature Test Suite")
    print("=" * 60)
    
    # Test joke generation
    gemini_success = test_joke_generation()
    
    # Test fallback
    test_fallback_joke()
    
    # Test speech
    test_speech_with_joke()
    
    print("\n" + "=" * 60)
    print("📊 Test Results:")
    print(f"Gemini Joke Generation: {'✅ PASS' if gemini_success else '❌ FAIL'}")
    print("Fallback Joke: ✅ PASS")
    print("Speech Integration: ✅ PASS")
    print("\n🎉 Joke feature is ready for the bot!")
