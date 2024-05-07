import pytest
from unittest.mock import patch, MagicMock
from flask import Flask
from core.apis.assignments.student import list_assignments, upsert_assignment, submit_assignment

@pytest.fixture
def app():
    # Create a Flask application context
    app = Flask(__name__)
    yield app

@pytest.fixture
def client(app):
    # Create a test client within the Flask application context
    with app.test_client() as client:
        yield client

@pytest.fixture
def mock_authenticated_principal():
    # Mocking an authenticated principal object
    return MagicMock()




