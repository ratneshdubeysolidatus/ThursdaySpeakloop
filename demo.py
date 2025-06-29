#!/usr/bin/env python3
"""
Demo script to test the ThursdaySpeakloop Bot behavior
This creates a mock Notion database scenario to test the auto-pause functionality
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
    print("=" * 50)
    
    teams = list(team_data.keys())
    random.shuffle(teams)
    total_teams = len(teams)
    
    for i, team in enumerate(teams, 1):
        print(f"\n🗣️ Team {team}, it's your turn.")
        time.sleep(1)
        
        selected_member = random.choice(team_data[team])
        print(f"🗣️ {selected_member}, please give your update.")
        time.sleep(2)
        
        if i < total_teams:
            print(f"🗣️ Team {team} update complete. Click Resume to continue to the next team.")
            print("⏸️ [AUTO-PAUSED] - Waiting for manual resume...")
            
            # Simulate waiting for user input
            input("   Press Enter to simulate 'Resume' button click...")
            print("▶️ Resumed by user.")
        else:
            print(f"🗣️ Team {team} update complete.")
    
    print("\n🗣️ Thanks everyone for your updates! All teams have presented. Have a great day!")
    print("✅ Bot completed successfully!")
    print("=" * 50)

if __name__ == "__main__":
    print("ThursdaySpeakloop Bot - Demo Mode")
    print("This simulates the new auto-pause after each team behavior\n")
    
    choice = input("Run demo? (y/n): ")
    if choice.lower() in ['y', 'yes']:
        simulate_meeting()
    else:
        print("Demo cancelled.")
