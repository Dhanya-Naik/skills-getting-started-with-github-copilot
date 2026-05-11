"""
Tests for DELETE /activities/{activity_name}/participants/{email} endpoint - remove students from activities.
Uses AAA (Arrange-Act-Assert) pattern for clarity.
"""

import pytest


def test_remove_participant_successful(client):
    """
    Test that a participant can be successfully removed from an activity.
    
    AAA Pattern:
    - Arrange: Setup client with existing activity and participant
    - Act: Make DELETE request to remove participant
    - Assert: Verify success response and participant is removed from list
    """
    # Arrange
    activity_name = "Chess Club"
    email_to_remove = "michael@mergington.edu"  # Already in participants per conftest
    
    # Verify email is in participants before removal
    activities_before = client.get("/activities").json()
    assert email_to_remove in activities_before[activity_name]["participants"]
    
    # Act
    response = client.delete(f"/activities/{activity_name}/participants/{email_to_remove}")
    
    # Assert - check response
    assert response.status_code == 200
    response_data = response.json()
    assert "message" in response_data
    assert email_to_remove in response_data["message"]
    
    # Assert - verify email was removed from participants
    activities_after = client.get("/activities").json()
    assert email_to_remove not in activities_after[activity_name]["participants"]


def test_remove_participant_activity_not_found(client):
    """
    Test that removing from a non-existent activity returns 404 error.
    
    AAA Pattern:
    - Arrange: Setup client with invalid activity name
    - Act: Make DELETE request for non-existent activity
    - Assert: Verify 404 status code and error message
    """
    # Arrange
    invalid_activity = "Non-Existent Activity"
    email = "student@mergington.edu"
    
    # Act
    response = client.delete(f"/activities/{invalid_activity}/participants/{email}")
    
    # Assert
    assert response.status_code == 404
    error_data = response.json()
    assert "detail" in error_data
    assert "not found" in error_data["detail"].lower()


def test_remove_participant_not_found(client):
    """
    Test that removing a non-existent participant returns 404 error.
    
    AAA Pattern:
    - Arrange: Setup valid activity but non-existent email
    - Act: Make DELETE request for email not in participants
    - Assert: Verify 404 status code and error message
    """
    # Arrange
    activity_name = "Chess Club"
    non_existent_email = "nonexistent@mergington.edu"
    
    # Act
    response = client.delete(f"/activities/{activity_name}/participants/{non_existent_email}")
    
    # Assert
    assert response.status_code == 404
    error_data = response.json()
    assert "detail" in error_data
    assert "not found" in error_data["detail"].lower()
