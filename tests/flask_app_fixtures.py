import pytest
from app import app


@pytest.fixture
def client():
    """Create a test client using Flask's built-in test client"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client
