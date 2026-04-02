"""Tests for DELETE /activities/{activity_name}/signup endpoint"""

def test_unregister_success(client):
    """Test successful unregistration from an activity"""
    # First signup
    client.post("/activities/Chess%20Club/signup?email=unregister@mergington.edu")

    # Then unregister
    response = client.delete("/activities/Chess%20Club/signup?email=unregister@mergington.edu")

    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "Unregistered unregister@mergington.edu from Chess Club" in data["message"]

    # Verify the participant was removed
    activities_response = client.get("/activities")
    activities = activities_response.json()
    assert "unregister@mergington.edu" not in activities["Chess Club"]["participants"]


def test_unregister_activity_not_found(client):
    """Test unregister from non-existent activity"""
    response = client.delete("/activities/NonExistent/signup?email=test@mergington.edu")

    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
    assert "Activity not found" in data["detail"]


def test_unregister_email_not_signed_up(client):
    """Test unregister with email not signed up for the activity"""
    response = client.delete("/activities/Chess%20Club/signup?email=notsignedup@mergington.edu")

    assert response.status_code == 400
    data = response.json()
    assert "detail" in data
    assert "Student is not signed up for this activity" in data["detail"]


def test_unregister_missing_email_parameter(client):
    """Test unregister without email parameter"""
    response = client.delete("/activities/Chess%20Club/signup")

    # FastAPI should return 422 for missing required query parameter
    assert response.status_code == 422


def test_unregister_empty_email(client):
    """Test unregister with empty email"""
    response = client.delete("/activities/Chess%20Club/signup?email=")

    # Currently succeeds but does nothing since empty email not in participants
    assert response.status_code == 200