#!/usr/bin/env python3
"""
Demo script to test the ThursdaySpeakloop Bot behavior
This creates a mock scenario to test the auto-pause and button state functionality
"""

import random
import time

def simulate_meeting():
    """Simulate a meeting with the new auto-pause behavior"""
    
    # Mock team data (similar to what would come from Notion)
    team_data = {
        "Frontend Team": ["Alice", "Bob", "Charlie"],
        "Backend Team": ["David", "Eve", "Frank"],
        "Mobile Team": ["Grace", "Henry", "Iris"],
        "DevOps Team": ["Jack", "Kelly"]
    }
    
    print("🎤 Starting ThursdaySpeakloop Bot Demo!")
    print("=" * 80)
    print("🔘 Start Bot button is now DISABLED")
    print("📊 Progress Panel is now VISIBLE")
    print("=" * 80)
    
    teams = list(team_data.keys())
    random.shuffle(teams)
    total_teams = len(teams)
    
    print(f"\n📊 Progress: 0 of {total_teams} teams completed (0%)")
    print("📍 Current Status: Initializing...")
    
    for i, team in enumerate(teams, 1):
        print(f"\n� Progress: {i-1} of {total_teams} teams completed ({((i-1)/total_teams)*100:.0f}%)")
        
        selected_member = random.choice(team_data[team])
        
        print(f"📍 Current Status: Announcing {team}")
        print(f"🏢 Current Team: {team}")
        print(f"👤 Speaking: -")
        print(f"�🗣️ Team {team}, it's your turn.")
        time.sleep(1)
        
        print(f"📍 Current Status: Calling {selected_member}")
        print(f"👤 Speaking: {selected_member}")
        print(f"🗣️ {selected_member}, please give your update.")
        time.sleep(2)
        
        print(f"📍 Current Status: {selected_member} is presenting")
        print("💬 [Team member gives update...]")
        time.sleep(1)
        
        if i < total_teams:
            print(f"� Current Status: Waiting for resume")
            print(f"�🗣️ Team {team} update complete.")
            print("⏸️ [AUTO-PAUSED] - Waiting for manual resume...")
            print("🌐 Web Interface: Resume button is now active")
            
            # Simulate waiting for user input
            input("   Press Enter to simulate 'Resume' button click...")
            print("▶️ Resumed by user.")
        else:
            print(f"📍 Current Status: {team} completed")
            print(f"🗣️ Team {team} update complete.")
    
    print(f"\n� Progress: {total_teams} of {total_teams} teams completed (100%)")
    print("📍 Current Status: All updates completed! 🎉")
    print("\n�🗣️ Thanks everyone for your updates! All teams have presented. Have a great day!")
    print("✅ Bot completed successfully!")
    print("=" * 80)
    print("🔘 Start Bot button is now ENABLED as 'Start New Session'")
    print("=" * 80)

def simulate_button_states():
    """Demonstrate the button state management"""
    print("\n🎮 Button State Management Demo:")
    print("=" * 40)
    
    states = [
        ("Initial State", "Start Bot - ENABLED"),
        ("Bot Starting", "Starting Bot... - DISABLED"),
        ("Bot Running", "Bot Running... - DISABLED"),
        ("Auto-Paused", "Bot Running... - DISABLED (Resume button active)"),
        ("Completed", "Start New Session - ENABLED"),
    ]
    
    for state, description in states:
        print(f"📍 {state}: {description}")
        time.sleep(1)

if __name__ == "__main__":
    print("ThursdaySpeakloop Bot - Enhanced Demo Mode")
    print("This simulates the new auto-pause and button management behavior\n")
    
    print("Available demos:")
    print("1. Full meeting simulation")
    print("2. Button state management demo")
    print("3. Both demos")
    
    choice = input("\nSelect demo (1/2/3) or 'q' to quit: ")
    
    if choice == '1':
        simulate_meeting()
    elif choice == '2':
        simulate_button_states()
    elif choice == '3':
        simulate_button_states()
        print("\n" + "="*60)
        simulate_meeting()
    elif choice.lower() == 'q':
        print("Demo cancelled.")
    else:
        print("Invalid choice. Demo cancelled.")
