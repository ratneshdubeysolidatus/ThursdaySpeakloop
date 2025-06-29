#!/usr/bin/env python3
"""
Enhanced Demo script showcasing Gemini AI voice features
This demonstrates the new expressive voice capabilities
"""

import random
import time
import os

def simulate_gemini_voices():
    """Demonstrate the variety of Gemini AI voices available"""
    print("🤖 Gemini AI Voice Options Demo")
    print("=" * 50)
    
    voices_with_personalities = {
        "Puck": "Upbeat - Perfect for welcoming and energetic announcements",
        "Kore": "Firm - Great for clear, authoritative team calls", 
        "Charon": "Informative - Ideal for detailed explanations",
        "Leda": "Youthful - Friendly and approachable tone",
        "Aoede": "Breezy - Light and casual for relaxed meetings",
        "Enceladus": "Breathy - Gentle and calming voice",
    }
    
    for voice, description in voices_with_personalities.items():
        print(f"🎭 {voice}: {description}")
        time.sleep(0.5)
    
    print("\n🎨 Style Options:")
    styles = [
        "Welcome: Enthusiastic, welcoming tone",
        "Friendly: Professional meeting facilitator tone", 
        "Encouraging: Supportive and motivating",
        "Completion: Warm, celebratory tone",
        "Transition: Smooth, transitional flow"
    ]
    
    for style in styles:
        print(f"   • {style}")
        time.sleep(0.3)

def simulate_enhanced_meeting():
    """Simulate a meeting with enhanced Gemini AI voices"""
    
    # Mock team data
    team_data = {
        "Frontend Team": ["Alice", "Bob", "Charlie"],
        "Backend Team": ["David", "Eve", "Frank"],
        "Mobile Team": ["Grace", "Henry", "Iris"],
        "DevOps Team": ["Jack", "Kelly"]
    }
    
    print("\n🎤 Enhanced ThursdaySpeakloop Bot Demo with Gemini AI!")
    print("=" * 70)
    
    gemini_enabled = os.getenv('GEMINI_API_KEY') is not None
    if gemini_enabled:
        print("🤖 Gemini AI: ENABLED - Enhanced expressive voices")
    else:
        print("📢 Gemini AI: DISABLED - Using pyttsx3 fallback")
        print("💡 Set GEMINI_API_KEY environment variable to enable AI voices")
    
    print("=" * 70)
    
    teams = list(team_data.keys())
    random.shuffle(teams)
    total_teams = len(teams)
    
    # Voice variety for different teams
    team_voices = ["Kore", "Puck", "Charon", "Leda", "Aoede", "Enceladus"]
    
    print(f"\n📊 Progress: 0 of {total_teams} teams completed (0%)")
    print("🎭 Voice: Puck (Upbeat)")
    print("🎨 Style: Welcome")
    print("🗣️ Starting ThursdaySpeakloop bot! [Enhanced AI voice with enthusiasm]")
    
    for i, team in enumerate(teams, 1):
        team_voice = team_voices[i % len(team_voices)]
        voice_desc = {
            "Kore": "Firm", "Puck": "Upbeat", "Charon": "Informative",
            "Leda": "Youthful", "Aoede": "Breezy", "Enceladus": "Breathy"
        }
        
        print(f"\n📊 Progress: {i-1} of {total_teams} teams completed ({((i-1)/total_teams)*100:.0f}%)")
        
        selected_member = random.choice(team_data[team])
        
        print(f"🎭 Voice: {team_voice} ({voice_desc[team_voice]})")
        print(f"🎨 Style: Friendly")
        print(f"📍 Current Status: Announcing {team}")
        print(f"🗣️ Team {team}, it's your turn. [Professional facilitator tone]")
        time.sleep(1)
        
        print(f"🎨 Style: Encouraging")
        print(f"📍 Current Status: Calling {selected_member}")
        print(f"🗣️ {selected_member}, please give your update. [Supportive, motivating tone]")
        time.sleep(2)
        
        print(f"📍 Current Status: {selected_member} is presenting")
        print("💬 [Team member gives update with enhanced background ambiance...]")
        time.sleep(1)
        
        if i < total_teams:
            print(f"🎨 Style: Transition")
            print(f"📍 Current Status: Waiting for resume")
            print("⏸️ [AUTO-PAUSED] - Smooth transitional voice guidance")
            print("🌐 Web Interface: Resume button is now active")
            
            input("   Press Enter to simulate 'Resume' button click...")
            print("▶️ Resumed by user.")
        else:
            print(f"🎨 Style: Completion")
            print(f"📍 Current Status: {team} completed")
            print(f"🗣️ Team {team} update complete. [Warm, celebratory tone]")
    
    print(f"\n📊 Progress: {total_teams} of {total_teams} teams completed (100%)")
    print("🎭 Voice: Puck (Upbeat)")
    print("🎨 Style: Completion")
    print("🗣️ Thanks everyone for your updates! All teams have presented. Have a great day!")
    print("   [Delivered with warm, celebratory AI-enhanced voice]")
    
    print("\n✅ Enhanced Meeting Complete!")
    print("=" * 70)
    print("🎯 Key AI Enhancements:")
    print("   • Dynamic voice selection per team")
    print("   • Context-aware emotional styling")
    print("   • Natural language prompts for expression")
    print("   • High-quality 24kHz audio output")
    print("   • Graceful fallback to pyttsx3 if needed")
    print("=" * 70)

def show_configuration_help():
    """Show how to configure Gemini AI"""
    print("\n⚙️ Configuration Guide")
    print("=" * 40)
    print("1. Get Gemini API Key:")
    print("   • Visit: https://aistudio.google.com/app/apikey")
    print("   • Create a new API key")
    print()
    print("2. Set Environment Variable:")
    print("   export GEMINI_API_KEY='your-api-key-here'")
    print()
    print("3. Or add to .env file:")
    print("   GEMINI_API_KEY=your-api-key-here")
    print()
    print("4. Test voices at:")
    print("   https://aistudio.google.com/generate-speech")

if __name__ == "__main__":
    print("ThursdaySpeakloop Bot - Enhanced AI Voice Demo")
    print("Showcasing Gemini AI's expressive speech capabilities\n")
    
    print("Available demos:")
    print("1. Voice options overview")
    print("2. Enhanced meeting simulation")
    print("3. Configuration help")
    print("4. All demos")
    
    choice = input("\nSelect demo (1/2/3/4) or 'q' to quit: ")
    
    if choice == '1':
        simulate_gemini_voices()
    elif choice == '2':
        simulate_enhanced_meeting()
    elif choice == '3':
        show_configuration_help()
    elif choice == '4':
        simulate_gemini_voices()
        print("\n" + "="*70)
        simulate_enhanced_meeting()
        show_configuration_help()
    elif choice.lower() == 'q':
        print("Demo cancelled.")
    else:
        print("Invalid choice. Demo cancelled.")
