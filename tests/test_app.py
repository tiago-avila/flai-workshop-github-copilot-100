"""
Unit tests for the Mergington High School Activities API
"""

import pytest
from fastapi.testclient import TestClient
import sys
from pathlib import Path

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from app import app, activities

client = TestClient(app)


@pytest.fixture(autouse=True)
def reset_activities():
    """Reset activities data before each test"""
    activities.clear()
    activities.update({
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
        }
    })
    yield


class TestGetActivities:
    """Tests for GET /activities endpoint"""

    def test_get_activities_success(self):
        """Test getting all activities"""
        response = client.get("/activities")
        assert response.status_code == 200
        data = response.json()
        assert "Chess Club" in data
        assert "Programming Class" in data
        assert "Gym Class" in data

    def test_activities_structure(self):
        """Test that activities have correct structure"""
        response = client.get("/activities")
        data = response.json()
        
        for activity_name, activity_data in data.items():
            assert "description" in activity_data
            assert "schedule" in activity_data
            assert "max_participants" in activity_data
            assert "participants" in activity_data
            assert isinstance(activity_data["participants"], list)


class TestSignupForActivity:
    """Tests for POST /activities/{activity_name}/signup endpoint"""

    def test_signup_success(self):
        """Test successful signup"""
        response = client.post(
            "/activities/Chess%20Club/signup",
            json={"email": "test@mergington.edu"}
        )
        assert response.status_code == 200
        assert "Successfully signed up" in response.json()["message"]
        assert "test@mergington.edu" in activities["Chess Club"]["participants"]

    def test_signup_invalid_email_domain(self):
        """Test signup with invalid email domain"""
        response = client.post(
            "/activities/Chess%20Club/signup",
            json={"email": "test@gmail.com"}
        )
        assert response.status_code == 422

    def test_signup_invalid_email_format(self):
        """Test signup with invalid email format"""
        response = client.post(
            "/activities/Chess%20Club/signup",
            json={"email": "notanemail"}
        )
        assert response.status_code == 422

    def test_signup_activity_not_found(self):
        """Test signup for non-existent activity"""
        response = client.post(
            "/activities/NonExistent/signup",
            json={"email": "test@mergington.edu"}
        )
        assert response.status_code == 404
        assert "Activity not found" in response.json()["detail"]

    def test_signup_duplicate_email(self):
        """Test duplicate signup"""
        # First signup
        client.post(
            "/activities/Chess%20Club/signup",
            json={"email": "test@mergington.edu"}
        )
        
        # Second signup with same email
        response = client.post(
            "/activities/Chess%20Club/signup",
            json={"email": "test@mergington.edu"}
        )
        assert response.status_code == 400
        assert "already signed up" in response.json()["detail"]

    def test_signup_activity_full(self):
        """Test signup when activity is full"""
        # Fill up Chess Club (max 12 participants)
        current_participants = activities["Chess Club"]["participants"]
        while len(current_participants) < 12:
            current_participants.append(f"student{len(current_participants)}@mergington.edu")
        
        # Try to sign up when full
        response = client.post(
            "/activities/Chess%20Club/signup",
            json={"email": "overflow@mergington.edu"}
        )
        assert response.status_code == 400
        assert "full" in response.json()["detail"].lower()

    def test_signup_case_insensitive_email(self):
        """Test that email is converted to lowercase"""
        response = client.post(
            "/activities/Chess%20Club/signup",
            json={"email": "Test@Mergington.edu"}
        )
        assert response.status_code == 200
        assert "test@mergington.edu" in activities["Chess Club"]["participants"]


class TestCancelSignup:
    """Tests for DELETE /activities/{activity_name}/signup endpoint"""

    def test_cancel_signup_success(self):
        """Test successful cancellation"""
        # First sign up
        client.post(
            "/activities/Chess%20Club/signup",
            json={"email": "test@mergington.edu"}
        )
        
        # Then cancel
        response = client.delete(
            "/activities/Chess%20Club/signup?email=test@mergington.edu"
        )
        assert response.status_code == 200
        assert "Successfully cancelled" in response.json()["message"]
        assert "test@mergington.edu" not in activities["Chess Club"]["participants"]

    def test_cancel_signup_not_enrolled(self):
        """Test cancellation when not enrolled"""
        response = client.delete(
            "/activities/Chess%20Club/signup?email=test@mergington.edu"
        )
        assert response.status_code == 404
        assert "not signed up" in response.json()["detail"]

    def test_cancel_signup_invalid_email_domain(self):
        """Test cancellation with invalid email domain"""
        response = client.delete(
            "/activities/Chess%20Club/signup?email=test@gmail.com"
        )
        assert response.status_code == 400
        assert "mergington.edu" in response.json()["detail"]

    def test_cancel_signup_activity_not_found(self):
        """Test cancellation for non-existent activity"""
        response = client.delete(
            "/activities/NonExistent/signup?email=test@mergington.edu"
        )
        assert response.status_code == 404
        assert "Activity not found" in response.json()["detail"]


class TestRootEndpoint:
    """Tests for GET / endpoint"""

    def test_root_redirects_to_static(self):
        """Test that root redirects to static index.html"""
        response = client.get("/", follow_redirects=False)
        assert response.status_code == 307
        assert response.headers["location"] == "/static/index.html"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
