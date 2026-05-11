"""
Tests for POST /activities/{activity_name}/signup endpoint - register students for activities.
Uses AAA (Arrange-Act-Assert) pattern for clarity.
"""

import pytest


def test_signup_successful(client):
    """
    Test that a student can successfully sign up for an activity.
    
    AAA Pattern:
    - Arrange: Setup fresh client, activity name, and new email address
    - Act: Make POST request to signup endpoint
    - Assert: Verify success response and email is added to participants
    """
    # Arrange
    activity_name = "Chess Club"
    new_email = "newstudent@mergington.edu"
    
    # Act
    response = client.post(f"/activities/{activity_name}/signup?email={new_email}")
    
    # Assert - check response
    assert response.status_code == 200
    response_data = response.json()
    assert "message" in response_data
    assert new_email in response_data["message"]
    
    # Assert - verify email was added to activity participants
    activities_response = client.get("/activities")
    activities = activities_response.json()
    assert new_email in activities[activity_name]["participants"]


def test_signup_activity_not_found(client):
    """
    Test that signing up for a non-existent activity returns 404 error.
    
    AAA Pattern:
    - Arrange: Setup client with invalid activity name
    - Act: Make POST request to non-existent activity
    - Assert: Verify 404 status code and error message
    """
    # Arrange
    invalid_activity = "Non-Existent Activity"
    email = "student@mergington.edu"
    
    # Act
    response = client.post(f"/activities/{invalid_activity}/signup?email={email}")
    
    # Assert
    assert response.status_code == 404
    error_data = response.json()
    assert "detail" in error_data
    assert "not found" in error_data["detail"].lower()


def test_signup_already_signed_up(client):
    """
    Test that a student who is already signed up gets a 400 error.
    
    AAA Pattern:
    - Arrange: Setup client and use email already in participants list
    - Act: Make POST request with email already signed up for activity
    - Assert: Verify 400 status code and error message
    """
    # Arrange
    activity_name = "Chess Club"
    existing_email = "michael@mergington.edu"  # Already signed up per conftest
    
    # Act
    response = client.post(f"/activities/{activity_name}/signup?email={existing_email}")
    
    # Assert
    assert response.status_code == 400
    error_data = response.json()
    assert "detail" in error_data
    assert "already signed up" in error_data["detail"].lower()
