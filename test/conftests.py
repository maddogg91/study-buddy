import pytest
import sys
import os
import requests


directory = os.path.dirname(os.path.realpath(__file__))

parent = os.path.dirname(directory)

sys.path.append(parent)
"""
from main import create_app

@pytest.fixture(scope='module')
def test_client():
    # Create a Flask app configured for testing
    flask_app = create_app()
    
     # Create a test client using the Flask application configured for testing
    with flask_app.test_client() as testing_client:
        # Establish an application context
        with flask_app.app_context():
            yield testing_client  # this is where the testing happens!

@pytest.fixture(scope='function')
def login_default_user(test_client):
    test_client.post('/login',
                     data= {"user": "TestUser1", "password": "Password"},
                     follow_redirects=True)

    yield  # this is where the testing happens!
"""
