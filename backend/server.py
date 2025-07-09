from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pymongo import MongoClient
from pydantic import BaseModel
from typing import Optional, List
import os
import asyncio
import uuid
from datetime import datetime, timedelta
import json

# Import Gemini integration
from emergentintegrations.llm.chat import LlmChat, UserMessage

app = FastAPI()

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database connection
MONGO_URL = os.environ.get('MONGO_URL', 'mongodb://localhost:27017')
DB_NAME = os.environ.get('DB_NAME', 'royal_attendant')

client = MongoClient(MONGO_URL)
db = client[DB_NAME]

# Collections
meetings = db.meetings
user_profiles = db.user_profiles
bunny_interactions = db.bunny_interactions
ai_summaries = db.ai_summaries

# Pydantic models
class Meeting(BaseModel):
    id: Optional[str] = None
    title: str
    date: str
    time: str
    timezone: str = "UTC"
    platform: str  # Zoom, Google Meet, Teams, etc.
    meeting_link: str
    meeting_id: Optional[str] = None
    passcode: Optional[str] = None
    host_name: str
    agenda: Optional[str] = None
    duration: int = 60  # minutes
    rsvp_status: str = "pending"
    mic_muted: bool = True
    camera_off: bool = True
    recurrence: str = "none"  # none, daily, weekly, custom
    reminder_times: List[int] = [5]  # minutes before
    backup_link: Optional[str] = None
    join_method: str = "browser"  # browser, desktop, ask
    waiting_room_message: Optional[str] = None
    attachments: List[str] = []
    created_at: Optional[datetime] = None
    status: str = "scheduled"  # scheduled, completed, cancelled

class UserProfile(BaseModel):
    id: Optional[str] = None
    name: str = "Joseph Onyango"
    email: Optional[str] = None
    avatar: Optional[str] = None
    theme: str = "starlight_grotto"
    bunny_outfit: str = "crown"
    bunny_companion: str = "lailan"
    preferred_platform: str = "zoom"
    reminder_voice: str = "fairy_chime"
    created_at: Optional[datetime] = None

class BunnyInteraction(BaseModel):
    id: Optional[str] = None
    user_id: str
    interaction_type: str  # joke, fact, trick, wisdom
    content: str
    gems_earned: int = 0
    timestamp: Optional[datetime] = None

class AISummary(BaseModel):
    id: Optional[str] = None
    meeting_id: str
    summary: str
    key_topics: List[str]
    decisions: List[str]
    action_items: List[str]
    created_at: Optional[datetime] = None

# Gemini AI Configuration
GEMINI_API_KEY = "AIzaSyAnj_tteByU7FPAMW5bSWdwRc9gLPcmRvE"

async def get_gemini_response(prompt: str, session_id: str = None) -> str:
    """Get response from Gemini AI"""
    try:
        if not session_id:
            session_id = str(uuid.uuid4())
        
        chat = LlmChat(
            api_key=GEMINI_API_KEY,
            session_id=session_id,
            system_message="You are a magical royal assistant named Lailan. You speak with enchanting wisdom and provide helpful, delightful responses with a touch of whimsy and sparkle."
        ).with_model("gemini", "gemini-2.0-flash")
        
        user_message = UserMessage(text=prompt)
        response = await chat.send_message(user_message)
        return response
    except Exception as e:
        return f"The magic crystal ball seems cloudy today... {str(e)}"

# API Routes

@app.get("/")
async def root():
    return {"message": "Welcome to the Prince Lailan Royal Attendant App! 🏰✨"}

# Meeting Management
@app.post("/api/meetings")
async def create_meeting(meeting: Meeting):
    """Create a new meeting"""
    meeting_dict = meeting.dict()
    meeting_dict["id"] = str(uuid.uuid4())
    meeting_dict["created_at"] = datetime.utcnow()
    
    result = meetings.insert_one(meeting_dict)
    return {"message": "Meeting scheduled successfully! 📜✨", "meeting_id": meeting_dict["id"]}

@app.get("/api/meetings")
async def get_meetings():
    """Get all meetings"""
    meetings_list = []
    for meeting in meetings.find():
        meeting["_id"] = str(meeting["_id"])
        meetings_list.append(meeting)
    return meetings_list

@app.get("/api/meetings/{meeting_id}")
async def get_meeting(meeting_id: str):
    """Get a specific meeting"""
    meeting = meetings.find_one({"id": meeting_id})
    if not meeting:
        raise HTTPException(status_code=404, detail="Meeting not found")
    meeting["_id"] = str(meeting["_id"])
    return meeting

@app.put("/api/meetings/{meeting_id}")
async def update_meeting(meeting_id: str, meeting: Meeting):
    """Update a meeting"""
    meeting_dict = meeting.dict()
    result = meetings.update_one({"id": meeting_id}, {"$set": meeting_dict})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Meeting not found")
    return {"message": "Meeting updated successfully! ✨"}

@app.delete("/api/meetings/{meeting_id}")
async def delete_meeting(meeting_id: str):
    """Delete a meeting"""
    result = meetings.delete_one({"id": meeting_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Meeting not found")
    return {"message": "Meeting cancelled successfully! 🗑️✨"}

# AI Features
@app.post("/api/ai/summarize")
async def summarize_meeting(meeting_id: str, transcript: str):
    """Generate AI summary for a meeting"""
    prompt = f"""
    As a royal scribe, please analyze this meeting transcript and provide:
    1. A concise summary
    2. Key topics discussed (as a list)
    3. Decisions made (as a list)
    4. Action items (as a list)
    
    Transcript: {transcript}
    
    Please format your response as JSON with these keys: summary, key_topics, decisions, action_items
    """
    
    response = await get_gemini_response(prompt)
    
    try:
        # Try to parse as JSON
        import json
        summary_data = json.loads(response)
    except:
        # If not JSON, create structured response
        summary_data = {
            "summary": response,
            "key_topics": [],
            "decisions": [],
            "action_items": []
        }
    
    # Save to database
    ai_summary = AISummary(
        meeting_id=meeting_id,
        summary=summary_data.get("summary", ""),
        key_topics=summary_data.get("key_topics", []),
        decisions=summary_data.get("decisions", []),
        action_items=summary_data.get("action_items", []),
        created_at=datetime.utcnow()
    )
    
    summary_dict = ai_summary.dict()
    summary_dict["id"] = str(uuid.uuid4())
    ai_summaries.insert_one(summary_dict)
    
    return summary_data

@app.get("/api/ai/joke")
async def get_daily_joke():
    """Get a magical daily joke"""
    prompt = "Tell me a cute, family-friendly joke with a magical or bunny theme. Keep it short and sweet!"
    response = await get_gemini_response(prompt)
    return {"joke": response}

@app.get("/api/ai/fluffy-fact")
async def get_fluffy_fact():
    """Get a fluffy fact of the day"""
    prompt = "Share an adorable, interesting fact about bunnies, magic, or nature. Make it delightful and educational!"
    response = await get_gemini_response(prompt)
    return {"fact": response}

@app.get("/api/ai/mindful-moment")
async def get_mindful_moment():
    """Get a mindful moment suggestion"""
    prompt = "Suggest a quick, magical 2-minute mindfulness or relaxation activity for someone working at their computer. Make it enchanting!"
    response = await get_gemini_response(prompt)
    return {"suggestion": response}

# Bunny Companion Features
@app.post("/api/bunny/interact")
async def bunny_interact(interaction_type: str, user_id: str = "default"):
    """Interact with Lailan's bunny companion"""
    prompts = {
        "joke": "Tell me a cute bunny joke!",
        "fact": "Share a fun fact about bunnies or magic!",
        "trick": "Describe a magical trick that Lailan the bunny performs!",
        "wisdom": "Share some gentle wisdom or encouragement for productivity!"
    }
    
    prompt = prompts.get(interaction_type, "Say something cute and encouraging!")
    response = await get_gemini_response(prompt)
    
    # Save interaction
    interaction = BunnyInteraction(
        user_id=user_id,
        interaction_type=interaction_type,
        content=response,
        gems_earned=1,
        timestamp=datetime.utcnow()
    )
    
    interaction_dict = interaction.dict()
    interaction_dict["id"] = str(uuid.uuid4())
    bunny_interactions.insert_one(interaction_dict)
    
    return {"response": response, "gems_earned": 1}

@app.get("/api/bunny/stats/{user_id}")
async def get_bunny_stats(user_id: str):
    """Get bunny interaction statistics"""
    total_interactions = bunny_interactions.count_documents({"user_id": user_id})
    total_gems = sum([interaction.get("gems_earned", 0) for interaction in bunny_interactions.find({"user_id": user_id})])
    
    return {
        "total_interactions": total_interactions,
        "total_gems": total_gems,
        "level": total_gems // 10 + 1,  # Level up every 10 gems
        "next_level_gems": ((total_gems // 10) + 1) * 10
    }

# User Profile Management
@app.get("/api/profile/{user_id}")
async def get_profile(user_id: str):
    """Get user profile"""
    profile = user_profiles.find_one({"id": user_id})
    if not profile:
        # Create default profile
        default_profile = UserProfile(id=user_id, created_at=datetime.utcnow())
        profile_dict = default_profile.dict()
        user_profiles.insert_one(profile_dict)
        return default_profile.dict()
    
    profile["_id"] = str(profile["_id"])
    return profile

@app.put("/api/profile/{user_id}")
async def update_profile(user_id: str, profile: UserProfile):
    """Update user profile"""
    profile_dict = profile.dict()
    result = user_profiles.update_one({"id": user_id}, {"$set": profile_dict}, upsert=True)
    return {"message": "Profile updated successfully! ✨"}

# Dashboard Data
@app.get("/api/dashboard")
async def get_dashboard_data():
    """Get dashboard data"""
    today = datetime.utcnow().date()
    
    # Today's meetings
    todays_meetings = []
    for meeting in meetings.find():
        meeting_date = datetime.strptime(meeting["date"], "%Y-%m-%d").date()
        if meeting_date == today:
            meeting["_id"] = str(meeting["_id"])
            todays_meetings.append(meeting)
    
    # Upcoming meetings (next 7 days)
    upcoming_meetings = []
    for meeting in meetings.find():
        meeting_date = datetime.strptime(meeting["date"], "%Y-%m-%d").date()
        if today < meeting_date <= today + timedelta(days=7):
            meeting["_id"] = str(meeting["_id"])
            upcoming_meetings.append(meeting)
    
    return {
        "todays_meetings": todays_meetings,
        "upcoming_meetings": upcoming_meetings,
        "total_meetings": meetings.count_documents({}),
        "greeting": f"Good day, Your Royal Highness! 👑✨"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)