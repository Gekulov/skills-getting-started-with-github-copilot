"""Tests for POST /activities/{activity_name}/signup endpoint"""

def test_signup_success(client):
    """Test successful signup for an activity"""
    response = client.post("/activities/Chess%20Club/signup?email=test@mergington.edu")

    assert response.status_code == 200
    data = response.json()

    assert "message" in data
    assert "Signed up test@mergington.edu for Chess Club" in data["message"]

    # Verify the participant was added
    activities_response = client.get("/activities")
    activities = activities_response.json()
    assert "test@mergington.edu" in activities["Chess Club"]["participants"]


def test_signup_activity_not_found(client):
    """Test signup for non-existent activity"""
    response = client.post("/activities/NonExistent/signup?email=test@mergington.edu")

    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
    assert "Activity not found" in data["detail"]


def test_signup_duplicate_email(client):
    """Test signup with email already registered for the activity"""
    # First signup
    client.post("/activities/Chess%20Club/signup?email=duplicate@mergington.edu")

    # Second signup with same email
    response = client.post("/activities/Chess%20Club/signup?email=duplicate@mergington.edu")

    assert response.status_code == 400
    data = response.json()
    assert "detail" in data
    assert "Student already signed up for this activity" in data["detail"]


def test_signup_different_activity_same_email(client):
    """Test that same email can signup for different activities"""
    # Signup for Chess Club
    response1 = client.post("/activities/Chess%20Club/signup?email=multi@mergington.edu")
    assert response1.status_code == 200

    # Signup for Programming Class with same email
    response2 = client.post("/activities/Programming%20Class/signup?email=multi@mergington.edu")
    assert response2.status_code == 200

    # Verify both activities have the participant
    activities_response = client.get("/activities")
    activities = activities_response.json()
    assert "multi@mergington.edu" in activities["Chess Club"]["participants"]
    assert "multi@mergington.edu" in activities["Programming Class"]["participants"]


def test_signup_missing_email_parameter(client):
    """Test signup without email parameter"""
    response = client.post("/activities/Chess%20Club/signup")

    # FastAPI should return 422 for missing required query parameter
    assert response.status_code == 422


def test_signup_empty_email(client):
    """Test signup with empty email"""
    response = client.post("/activities/Chess%20Club/signup?email=")

    # This might succeed or fail depending on validation, but let's test current behavior
    # Currently no validation, so it succeeds
    assert response.status_code == 200