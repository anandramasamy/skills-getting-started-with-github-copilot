"""Tests for the FastAPI endpoints using the Arrange-Act-Assert pattern."""

from src import app as app_module


def test_get_activities(client):
    # Arrange: nothing to set up beyond the fixture-provided client

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    data = response.json()
    # we expect the hard-coded keys to be present
    assert "Chess Club" in data
    assert isinstance(data["Chess Club"], dict)
    assert "participants" in data["Chess Club"]


def test_signup_success(client):
    # Arrange
    activity = "Chess Club"
    email = "newstudent@mergington.edu"
    assert email not in app_module.activities[activity]["participants"]

    # Act
    response = client.post(
        f"/activities/{activity}/signup",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 200
    payload = response.json()
    assert "Signed up" in payload["message"]
    assert email in app_module.activities[activity]["participants"]


def test_signup_duplicate(client):
    # Arrange
    activity = "Chess Club"
    email = app_module.activities[activity]["participants"][0]

    # Act
    response = client.post(
        f"/activities/{activity}/signup",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"]


def test_delete_participant_success(client):
    # Arrange
    activity = "Chess Club"
    email = app_module.activities[activity]["participants"][0]
    assert email in app_module.activities[activity]["participants"]

    # Act
    response = client.delete(
        f"/activities/{activity}/participants",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 200
    assert email not in app_module.activities[activity]["participants"]
    assert "Removed" in response.json()["message"]


def test_delete_nonexistent(client):
    # Arrange
    missing_activity = "Nonexistent"
    bad_email = "nobody@nowhere.edu"

    # Act
    resp1 = client.delete(
        f"/activities/{missing_activity}/participants",
        params={"email": bad_email},
    )
    resp2 = client.delete(
        "/activities/Chess Club/participants",
        params={"email": bad_email},
    )

    # Assert
    assert resp1.status_code == 404
    assert resp2.status_code == 404
