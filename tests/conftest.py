import copy

import pytest

from src import app as app_module


@pytest.fixture(autouse=True)
def restore_activities():
    """Ensure the global ``activities`` dict is reset between tests.

    The FastAPI app stores all activity state in a module‑level dictionary, which
    would be mutated as tests add/remove participants.  Copy the original data
    before the test and restore it afterward so each case starts clean.  The
    fixture is ``autouse`` so every test gets a fresh state automatically.
    """
    original = copy.deepcopy(app_module.activities)
    yield
    app_module.activities = original


@pytest.fixture
def client():
    """Return a ``TestClient`` for exercising the FastAPI application."""
    from fastapi.testclient import TestClient

    return TestClient(app_module.app)
