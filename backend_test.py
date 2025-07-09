#!/usr/bin/env python3
import requests
import json
import time
import uuid
from datetime import datetime, timedelta
import os
import sys

# Get the backend URL from frontend/.env
BACKEND_URL = None
try:
    with open('/app/frontend/.env', 'r') as f:
        for line in f:
            if line.startswith('REACT_APP_BACKEND_URL='):
                BACKEND_URL = line.strip().split('=')[1].strip('"\'')
                break
    
    if not BACKEND_URL:
        print("❌ ERROR: Could not find REACT_APP_BACKEND_URL in frontend/.env")
        sys.exit(1)
except Exception as e:
    print(f"❌ ERROR: Could not read frontend/.env: {e}")
    sys.exit(1)

print(f"🔍 Using backend URL: {BACKEND_URL}")

# Test results tracking
test_results = {
    "meeting_management": {
        "create_meeting": False,
        "get_meetings": False,
        "get_meeting": False,
        "update_meeting": False,
        "delete_meeting": False
    },
    "ai_integration": {
        "summarize_meeting": False,
        "get_joke": False,
        "get_fluffy_fact": False,
        "get_mindful_moment": False
    },
    "bunny_companion": {
        "interact": False,
        "get_stats": False
    },
    "user_profiles": {
        "get_profile": False,
        "update_profile": False
    },
    "dashboard": {
        "get_dashboard_data": False
    }
}

# Test data
test_user_id = str(uuid.uuid4())
test_meeting_id = None

def print_separator():
    print("\n" + "="*80 + "\n")

def test_meeting_management():
    global test_meeting_id
    print_separator()
    print("🧪 Testing Meeting Management APIs")
    
    # Test creating a meeting
    print("\n📝 Testing POST /api/meetings")
    meeting_data = {
        "title": "Royal Strategy Session",
        "date": (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d"),
        "time": "14:30",
        "timezone": "UTC",
        "platform": "Zoom",
        "meeting_link": "https://zoom.us/j/123456789",
        "meeting_id": "123456789",
        "passcode": "royal123",
        "host_name": "Prince Lailan",
        "agenda": "Discuss kingdom expansion and magical innovations",
        "duration": 60,
        "rsvp_status": "confirmed",
        "mic_muted": True,
        "camera_off": False,
        "recurrence": "weekly",
        "reminder_times": [5, 15, 30],
        "backup_link": "https://teams.microsoft.com/l/meetup-join/123",
        "join_method": "browser",
        "waiting_room_message": "Welcome to the royal meeting! The prince will admit you shortly.",
        "attachments": ["kingdom_map.pdf", "magical_innovations.pptx"]
    }
    
    try:
        response = requests.post(f"{BACKEND_URL}/api/meetings", json=meeting_data)
        response.raise_for_status()
        result = response.json()
        test_meeting_id = result.get("meeting_id")
        
        if test_meeting_id and "Meeting scheduled successfully" in result.get("message", ""):
            print(f"✅ Successfully created meeting with ID: {test_meeting_id}")
            test_results["meeting_management"]["create_meeting"] = True
        else:
            print(f"❌ Failed to create meeting: {result}")
    except Exception as e:
        print(f"❌ Error creating meeting: {e}")
    
    # Test getting all meetings
    print("\n📝 Testing GET /api/meetings")
    try:
        response = requests.get(f"{BACKEND_URL}/api/meetings")
        response.raise_for_status()
        meetings = response.json()
        
        if isinstance(meetings, list):
            print(f"✅ Successfully retrieved {len(meetings)} meetings")
            test_results["meeting_management"]["get_meetings"] = True
        else:
            print(f"❌ Failed to retrieve meetings: {meetings}")
    except Exception as e:
        print(f"❌ Error retrieving meetings: {e}")
    
    # Test getting a specific meeting
    if test_meeting_id:
        print(f"\n📝 Testing GET /api/meetings/{test_meeting_id}")
        try:
            response = requests.get(f"{BACKEND_URL}/api/meetings/{test_meeting_id}")
            response.raise_for_status()
            meeting = response.json()
            
            if meeting and meeting.get("id") == test_meeting_id:
                print(f"✅ Successfully retrieved meeting: {meeting.get('title')}")
                test_results["meeting_management"]["get_meeting"] = True
            else:
                print(f"❌ Failed to retrieve meeting: {meeting}")
        except Exception as e:
            print(f"❌ Error retrieving meeting: {e}")
    
    # Test updating a meeting
    if test_meeting_id:
        print(f"\n📝 Testing PUT /api/meetings/{test_meeting_id}")
        
        # First get the current meeting to preserve its ID
        try:
            response = requests.get(f"{BACKEND_URL}/api/meetings/{test_meeting_id}")
            response.raise_for_status()
            current_meeting = response.json()
            
            # Prepare update data while preserving the ID
            update_data = {
                "id": test_meeting_id,  # Explicitly include the ID
                "title": "Updated Royal Strategy Session",
                "date": (datetime.now() + timedelta(days=2)).strftime("%Y-%m-%d"),
                "time": "15:30",
                "timezone": "UTC",
                "platform": "Zoom",
                "meeting_link": "https://zoom.us/j/123456789",
                "meeting_id": "123456789",
                "passcode": "royal123",
                "host_name": "Prince Lailan",
                "agenda": "Updated agenda with magical focus",
                "duration": 90,
                "rsvp_status": "confirmed",
                "mic_muted": True,
                "camera_off": False,
                "recurrence": "weekly",
                "reminder_times": [5, 15, 30],
                "backup_link": "https://teams.microsoft.com/l/meetup-join/123",
                "join_method": "browser",
                "waiting_room_message": "Welcome to the royal meeting! The prince will admit you shortly.",
                "attachments": ["kingdom_map.pdf", "magical_innovations.pptx"]
            }
            
            response = requests.put(f"{BACKEND_URL}/api/meetings/{test_meeting_id}", json=update_data)
            response.raise_for_status()
            result = response.json()
            
            if "Meeting updated successfully" in result.get("message", ""):
                print(f"✅ Successfully updated meeting")
                test_results["meeting_management"]["update_meeting"] = True
            else:
                print(f"❌ Failed to update meeting: {result}")
        except Exception as e:
            print(f"❌ Error updating meeting: {e}")
    
    # Test deleting a meeting
    if test_meeting_id:
        print(f"\n📝 Testing DELETE /api/meetings/{test_meeting_id}")
        try:
            response = requests.delete(f"{BACKEND_URL}/api/meetings/{test_meeting_id}")
            response.raise_for_status()
            result = response.json()
            
            if "Meeting cancelled successfully" in result.get("message", ""):
                print(f"✅ Successfully deleted meeting")
                test_results["meeting_management"]["delete_meeting"] = True
            else:
                print(f"❌ Failed to delete meeting: {result}")
        except Exception as e:
            print(f"❌ Error deleting meeting: {e}")

def test_ai_integration():
    global test_meeting_id
    print_separator()
    print("🧪 Testing AI Integration APIs")
    
    # Create a test meeting for AI summary
    meeting_data = {
        "title": "AI Test Meeting",
        "date": datetime.now().strftime("%Y-%m-%d"),
        "time": "10:00",
        "timezone": "UTC",
        "platform": "Zoom",
        "meeting_link": "https://zoom.us/j/987654321",
        "host_name": "AI Tester"
    }
    
    try:
        response = requests.post(f"{BACKEND_URL}/api/meetings", json=meeting_data)
        response.raise_for_status()
        result = response.json()
        ai_test_meeting_id = result.get("meeting_id")
        print(f"✅ Created test meeting for AI summary with ID: {ai_test_meeting_id}")
    except Exception as e:
        print(f"❌ Error creating test meeting for AI summary: {e}")
        ai_test_meeting_id = None
    
    # Test AI meeting summary
    if ai_test_meeting_id:
        print("\n📝 Testing POST /api/ai/summarize")
        transcript = """
        Prince Lailan: Welcome everyone to our royal meeting. Today we'll discuss the enchanted forest expansion.
        Royal Advisor: Your Highness, we've surveyed the northern borders and found suitable land.
        Court Magician: The magical energy readings are strong there, perfect for our new enchantments.
        Prince Lailan: Excellent! Let's proceed with the expansion plans. We'll need to allocate resources.
        Royal Treasurer: I suggest we use 500 gold coins from the royal treasury for this project.
        Prince Lailan: Approved. Let's also ensure we're respectful of the forest creatures.
        Court Naturalist: We'll implement our eco-friendly magical construction methods.
        Prince Lailan: Perfect! Our action items are: 1) Begin surveying next week, 2) Allocate 500 gold coins, 3) Prepare eco-friendly enchantments.
        Everyone: Agreed!
        """
        
        try:
            # Use query parameters for both meeting_id and transcript
            response = requests.post(
                f"{BACKEND_URL}/api/ai/summarize?meeting_id={ai_test_meeting_id}&transcript={transcript}"
            )
            
            response.raise_for_status()
            summary = response.json()
            
            if summary and "summary" in summary:
                print(f"✅ Successfully generated meeting summary")
                test_results["ai_integration"]["summarize_meeting"] = True
            else:
                print(f"❌ Failed to generate meeting summary: {summary}")
        except Exception as e:
            print(f"❌ Error generating meeting summary: {e}")
            print(f"Response status code: {getattr(response, 'status_code', 'N/A')}")
            print(f"Response text: {getattr(response, 'text', 'N/A')}")
    
    # Test getting a joke
    print("\n📝 Testing GET /api/ai/joke")
    try:
        response = requests.get(f"{BACKEND_URL}/api/ai/joke")
        response.raise_for_status()
        joke = response.json()
        
        if joke and "joke" in joke:
            print(f"✅ Successfully retrieved joke: {joke['joke'][:50]}...")
            test_results["ai_integration"]["get_joke"] = True
        else:
            print(f"❌ Failed to retrieve joke: {joke}")
    except Exception as e:
        print(f"❌ Error retrieving joke: {e}")
    
    # Test getting a fluffy fact
    print("\n📝 Testing GET /api/ai/fluffy-fact")
    try:
        response = requests.get(f"{BACKEND_URL}/api/ai/fluffy-fact")
        response.raise_for_status()
        fact = response.json()
        
        if fact and "fact" in fact:
            print(f"✅ Successfully retrieved fluffy fact: {fact['fact'][:50]}...")
            test_results["ai_integration"]["get_fluffy_fact"] = True
        else:
            print(f"❌ Failed to retrieve fluffy fact: {fact}")
    except Exception as e:
        print(f"❌ Error retrieving fluffy fact: {e}")
    
    # Test getting a mindful moment
    print("\n📝 Testing GET /api/ai/mindful-moment")
    try:
        response = requests.get(f"{BACKEND_URL}/api/ai/mindful-moment")
        response.raise_for_status()
        moment = response.json()
        
        if moment and "suggestion" in moment:
            print(f"✅ Successfully retrieved mindful moment: {moment['suggestion'][:50]}...")
            test_results["ai_integration"]["get_mindful_moment"] = True
        else:
            print(f"❌ Failed to retrieve mindful moment: {moment}")
    except Exception as e:
        print(f"❌ Error retrieving mindful moment: {e}")

def test_bunny_companion():
    print_separator()
    print("🧪 Testing Bunny Companion APIs")
    
    # Test bunny interaction
    print("\n📝 Testing POST /api/bunny/interact")
    interaction_types = ["joke", "fact", "trick", "wisdom"]
    
    for interaction_type in interaction_types:
        try:
            response = requests.post(f"{BACKEND_URL}/api/bunny/interact", params={"interaction_type": interaction_type, "user_id": test_user_id})
            response.raise_for_status()
            result = response.json()
            
            if result and "response" in result and "gems_earned" in result:
                print(f"✅ Successfully interacted with bunny ({interaction_type}): {result['response'][:50]}...")
                test_results["bunny_companion"]["interact"] = True
            else:
                print(f"❌ Failed to interact with bunny ({interaction_type}): {result}")
        except Exception as e:
            print(f"❌ Error interacting with bunny ({interaction_type}): {e}")
    
    # Test getting bunny stats
    print(f"\n📝 Testing GET /api/bunny/stats/{test_user_id}")
    try:
        response = requests.get(f"{BACKEND_URL}/api/bunny/stats/{test_user_id}")
        response.raise_for_status()
        stats = response.json()
        
        if stats and "total_interactions" in stats and "total_gems" in stats:
            print(f"✅ Successfully retrieved bunny stats: {stats}")
            test_results["bunny_companion"]["get_stats"] = True
        else:
            print(f"❌ Failed to retrieve bunny stats: {stats}")
    except Exception as e:
        print(f"❌ Error retrieving bunny stats: {e}")

def test_user_profiles():
    print_separator()
    print("🧪 Testing User Profile APIs")
    
    # Test getting user profile
    print(f"\n📝 Testing GET /api/profile/{test_user_id}")
    try:
        response = requests.get(f"{BACKEND_URL}/api/profile/{test_user_id}")
        response.raise_for_status()
        profile = response.json()
        
        if profile and "id" in profile:
            print(f"✅ Successfully retrieved user profile: {profile}")
            test_results["user_profiles"]["get_profile"] = True
        else:
            print(f"❌ Failed to retrieve user profile: {profile}")
    except Exception as e:
        print(f"❌ Error retrieving user profile: {e}")
    
    # Test updating user profile
    print(f"\n📝 Testing PUT /api/profile/{test_user_id}")
    profile_data = {
        "name": "Royal Tester",
        "email": "tester@royal-kingdom.com",
        "theme": "enchanted_forest",
        "bunny_outfit": "wizard_hat",
        "bunny_companion": "lailan",
        "preferred_platform": "teams",
        "reminder_voice": "magical_bell"
    }
    
    try:
        response = requests.put(f"{BACKEND_URL}/api/profile/{test_user_id}", json=profile_data)
        response.raise_for_status()
        result = response.json()
        
        if "Profile updated successfully" in result.get("message", ""):
            print(f"✅ Successfully updated user profile")
            test_results["user_profiles"]["update_profile"] = True
        else:
            print(f"❌ Failed to update user profile: {result}")
    except Exception as e:
        print(f"❌ Error updating user profile: {e}")

def test_dashboard():
    print_separator()
    print("🧪 Testing Dashboard API")
    
    # Test getting dashboard data
    print("\n📝 Testing GET /api/dashboard")
    try:
        response = requests.get(f"{BACKEND_URL}/api/dashboard")
        response.raise_for_status()
        dashboard = response.json()
        
        if dashboard and "todays_meetings" in dashboard and "upcoming_meetings" in dashboard:
            print(f"✅ Successfully retrieved dashboard data")
            print(f"   Today's meetings: {len(dashboard['todays_meetings'])}")
            print(f"   Upcoming meetings: {len(dashboard['upcoming_meetings'])}")
            print(f"   Total meetings: {dashboard['total_meetings']}")
            print(f"   Greeting: {dashboard['greeting']}")
            test_results["dashboard"]["get_dashboard_data"] = True
        else:
            print(f"❌ Failed to retrieve dashboard data: {dashboard}")
    except Exception as e:
        print(f"❌ Error retrieving dashboard data: {e}")

def print_test_summary():
    print_separator()
    print("📊 TEST SUMMARY")
    print_separator()
    
    all_passed = True
    
    for category, tests in test_results.items():
        print(f"\n{category.upper()}:")
        for test, passed in tests.items():
            status = "✅ PASSED" if passed else "❌ FAILED"
            print(f"  {test}: {status}")
            if not passed:
                all_passed = False
    
    print_separator()
    if all_passed:
        print("🎉 ALL TESTS PASSED! The Prince Lailan Royal Attendant App backend is working correctly.")
    else:
        print("⚠️ SOME TESTS FAILED. Please check the detailed results above.")
    print_separator()

def main():
    print("🏰✨ PRINCE LAILAN ROYAL ATTENDANT APP - BACKEND TESTS ✨🏰")
    print(f"Starting tests at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Run all tests
    test_meeting_management()
    test_ai_integration()
    test_bunny_companion()
    test_user_profiles()
    test_dashboard()
    
    # Print summary
    print_test_summary()

if __name__ == "__main__":
    main()