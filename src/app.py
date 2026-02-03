"""
High School Management System API

A super simple FastAPI application that allows students to view and sign up
for extracurricular activities at Mergington High School.
"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from pydantic import BaseModel, EmailStr, validator
import os
from pathlib import Path
import re

app = FastAPI(title="Mergington High School API",
              description="API for viewing and signing up for extracurricular activities")

# Mount the static files directory
current_dir = Path(__file__).parent
app.mount("/static", StaticFiles(directory=os.path.join(Path(__file__).parent,
          "static")), name="static")

# In-memory activity database
activities = {
    "Chess Club": {
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
    },
    "Programming Class": {
        "description": "Learn programming fundamentals and build software projects",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
    },
    "Gym Class": {
        "description": "Physical education and sports activities",
        "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
        "max_participants": 30,
        "participants": ["john@mergington.edu", "olivia@mergington.edu"]
    },
    "Drama Club": {
        "description": "Theater performances, acting workshops, and stage productions",
        "schedule": "Wednesdays, 4:00 PM - 6:00 PM",
        "max_participants": 15,
        "participants": ["sarah@mergington.edu"]
    },
    "Debate Team": {
        "description": "Develop critical thinking and public speaking skills",
        "schedule": "Thursdays, 3:30 PM - 5:00 PM",
        "max_participants": 16,
        "participants": ["alex@mergington.edu", "maria@mergington.edu"]
    },
    "Art Club": {
        "description": "Explore various art forms including painting, drawing, and sculpture",
        "schedule": "Mondays, 3:30 PM - 5:00 PM",
        "max_participants": 18,
        "participants": []
    }
}


class SignupRequest(BaseModel):
    email: EmailStr
    
    @validator('email')
    def validate_mergington_email(cls, v):
        if not v.endswith('@mergington.edu'):
            raise ValueError('Email must be from mergington.edu domain')
        return v.lower()


@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")


@app.get("/activities")
def get_activities():
    """Get all available activities"""
    return activities


@app.post("/activities/{activity_name}/signup")
def signup_for_activity(activity_name: str, signup: SignupRequest):
    """Sign up a student for an activity"""
    # Validate activity exists
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    # Get the specific activity
    activity = activities[activity_name]
    email = signup.email.lower()
    
    # Check if student is already signed up
    if email in activity["participants"]:
        raise HTTPException(status_code=400, detail="You are already signed up for this activity")
    
    # Check if activity is full
    if len(activity["participants"]) >= activity["max_participants"]:
        raise HTTPException(status_code=400, detail="This activity is full")

    # Add student
    activity["participants"].append(email)
    return {"message": f"Successfully signed up {email} for {activity_name}"}


@app.delete("/activities/{activity_name}/signup")
def cancel_signup(activity_name: str, email: str):
    """Cancel a student's signup for an activity"""
    # Validate activity exists
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")
    
    # Validate email format
    if not email.endswith('@mergington.edu'):
        raise HTTPException(status_code=400, detail="Email must be from mergington.edu domain")
    
    # Get the specific activity
    activity = activities[activity_name]
    email = email.lower()
    
    # Check if student is signed up
    if email not in activity["participants"]:
        raise HTTPException(status_code=404, detail="You are not signed up for this activity")
    
    # Remove student
    activity["participants"].remove(email)
    return {"message": f"Successfully cancelled signup for {activity_name}"}
