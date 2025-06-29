#!/usr/bin/env python3
"""
Quick test to check speech functionality
"""

import os
import pyttsx3
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_pyttsx3():
    """Test basic pyttsx3 speech"""
    print("🧪 Testing pyttsx3 speech...")
    try:
        engine = pyttsx3.init()
        engine.say("Hello, this is a test of pyttsx3 speech.")
        engine.runAndWait()
        print("✅ pyttsx3 speech working!")
        return True
    except Exception as e:
        print(f"❌ pyttsx3 error: {e}")
        return False

def test_gemini_api():
    """Test Gemini API connection"""
    print("🧪 Testing Gemini API connection...")
    api_key = os.getenv('GEMINI_API_KEY')
    
    if not api_key:
        print("❌ No GEMINI_API_KEY found in environment")
        return False
    
    print(f"✅ GEMINI_API_KEY found (starts with: {api_key[:10]}...)")
    
    try:
        from google import genai
        client = genai.Client(api_key=api_key)
        print("✅ Gemini client initialized successfully")
        return True
    except Exception as e:
        print(f"❌ Gemini API error: {e}")
        return False

def test_environment():
    """Test environment loading"""
    print("🧪 Testing environment variables...")
    
    notion_token = os.getenv('NOTION_TOKEN')
    database_id = os.getenv('DATABASE_ID')
    gemini_key = os.getenv('GEMINI_API_KEY')
    
    print(f"NOTION_TOKEN: {'✅ Set' if notion_token else '❌ Missing'}")
    print(f"DATABASE_ID: {'✅ Set' if database_id else '❌ Missing'}")
    print(f"GEMINI_API_KEY: {'✅ Set' if gemini_key else '❌ Missing'}")
    
    return all([notion_token, database_id])

if __name__ == "__main__":
    print("🔊 Speech System Diagnostic")
    print("=" * 40)
    
    # Test environment
    env_ok = test_environment()
    print()
    
    # Test speech systems
    pyttsx3_ok = test_pyttsx3()
    print()
    
    gemini_ok = test_gemini_api()
    print()
    
    print("=" * 40)
    print("📊 Diagnostic Results:")
    print(f"Environment: {'✅' if env_ok else '❌'}")
    print(f"pyttsx3: {'✅' if pyttsx3_ok else '❌'}")
    print(f"Gemini AI: {'✅' if gemini_ok else '❌'}")
    
    if pyttsx3_ok or gemini_ok:
        print("\n✅ Speech system is functional!")
    else:
        print("\n❌ No working speech system found!")
