"""
Tests for GET /activities endpoint - retrieve all extracurricular activities.
Uses AAA (Arrange-Act-Assert) pattern for clarity.
"""

import pytest


def test_get_activities_returns_all_activities(client):
    """
    Test that GET /activities returns all activities from the database.
    
    AAA Pattern:
    - Arrange: Using client fixture with sample_activities already loaded
    - Act: Make GET request to /activities
    - Assert: Verify status code and response contains expected activities
    """
    # Arrange
    # (client fixture already has activities loaded via monkeypatch)
    
    # Act
    response = client.get("/activities")
    
    # Assert
    assert response.status_code == 200
    activities = response.json()
    assert "Chess Club" in activities
    assert "Programming Class" in activities
    assert "Gym Class" in activities
    assert len(activities) == 3


def test_get_activities_structure(client):
    """
    Test that each activity in the response has the required fields.
    
    AAA Pattern:
    - Arrange: Using client fixture with sample_activities
    - Act: Make GET request and extract first activity
    - Assert: Verify all required fields are present with correct data types
    """
    # Arrange
    # (client fixture already has activities loaded)
    
    # Act
    response = client.get("/activities")
    activities = response.json()
    chess_club = activities["Chess Club"]
    
    # Assert - check required fields exist
    assert "description" in chess_club
    assert "schedule" in chess_club
    assert "max_participants" in chess_club
    assert "participants" in chess_club
    
    # Assert - check field types and values
    assert isinstance(chess_club["description"], str)
    assert isinstance(chess_club["schedule"], str)
    assert isinstance(chess_club["max_participants"], int)
    assert isinstance(chess_club["participants"], list)
    assert chess_club["max_participants"] == 12
    assert len(chess_club["participants"]) == 2
