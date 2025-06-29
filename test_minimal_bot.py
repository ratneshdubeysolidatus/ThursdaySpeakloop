#!/usr/bin/env python3
"""
Minimal bot test focused on speech functionality
"""

import os
import sys
from dotenv import load_dotenv

load_dotenv()

# Test if we can run the speaker bot with minimal setup
def test_minimal_bot():
    print("🧪 Testing Minimal Bot with Speech")
    print("=" * 50)
    
    # Check if we have the required credentials
    notion_token = os.getenv('NOTION_TOKEN')
    database_id = os.getenv('DATABASE_ID')
    
    if not notion_token or not database_id:
        print("❌ Missing Notion credentials")
        return False
    
    print("✅ Notion credentials found")
    
    # Import and test the speaker bot function
    try:
        from speaker_bot import run_speaker_bot
        print("✅ speaker_bot module imported successfully")
        
        # Test with a simple voice
        print("🎤 Testing with Puck voice...")
        
        # This should speak the welcome message at minimum
        print("🚀 Starting bot test...")
        run_speaker_bot(notion_token, database_id, "Puck")
        
    except Exception as e:
        print(f"❌ Bot test failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

if __name__ == "__main__":
    test_minimal_bot()
