"""Tests for GET /activities endpoint"""

def test_get_activities_success(client):
    """Test successful retrieval of all activities"""
    response = client.get("/activities")

    assert response.status_code == 200
    data = response.json()

    # Should return a dictionary
    assert isinstance(data, dict)

    # Should have all 9 activities
    assert len(data) == 9

    # Check structure of one activity
    chess_club = data["Chess Club"]
    assert "description" in chess_club
    assert "schedule" in chess_club
    assert "max_participants" in chess_club
    assert "participants" in chess_club

    # Check specific values
    assert chess_club["description"] == "Learn strategies and compete in chess tournaments"
    assert chess_club["max_participants"] == 12
    assert "michael@mergington.edu" in chess_club["participants"]


def test_get_activities_structure(client):
    """Test that activities have correct structure"""
    response = client.get("/activities")
    data = response.json()

    for activity_name, activity_data in data.items():
        assert isinstance(activity_name, str)
        assert isinstance(activity_data, dict)

        required_fields = ["description", "schedule", "max_participants", "participants"]
        for field in required_fields:
            assert field in activity_data

        assert isinstance(activity_data["description"], str)
        assert isinstance(activity_data["schedule"], str)
        assert isinstance(activity_data["max_participants"], int)
        assert isinstance(activity_data["participants"], list)

        # Participants should be list of strings (emails)
        for participant in activity_data["participants"]:
            assert isinstance(participant, str)
            assert "@" in participant  # Basic email validation


def test_root_redirect(client):
    """Test that root endpoint redirects to static index"""
    response = client.get("/", follow_redirects=False)

    assert response.status_code == 307  # Temporary redirect
    assert response.headers["location"] == "/static/index.html"