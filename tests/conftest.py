"""
Pytest configuration and shared fixtures for FastAPI application tests.
"""

import pytest
from fastapi.testclient import TestClient
from src.app import app
import src.app as app_module


@pytest.fixture
def sample_activities():
    """
    Provide a fresh copy of test activities for each test.
    This ensures test isolation - tests don't affect each other's state.
    """
    return {
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
            "participants": ["emma@mergington.edu"]
        },
        "Gym Class": {
            "description": "Physical education and sports activities",
            "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
            "max_participants": 30,
            "participants": ["john@mergington.edu"]
        }
    }


@pytest.fixture
def client(monkeypatch, sample_activities):
    """
    Provide a TestClient instance with isolated activities state.
    
    Before each test, replaces the module-level activities dict with a fresh copy.
    This ensures tests are isolated - changes in one test don't affect others.
    """
    # Replace the activities dict in the app module with our test data
    monkeypatch.setattr(app_module, "activities", sample_activities)
    
    # Return the TestClient
    return TestClient(app)
