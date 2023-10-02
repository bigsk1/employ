from flask import Flask
import pytest
import sys

# Add the parent directory to the PYTHONPATH to find the app module
sys.path.append("..")

# Import your Flask app from app.py
from .app import app as flask_app

def test_app_exists():
    assert flask_app is not None

def test_app_is_instance_of_flask():
    assert isinstance(flask_app, Flask)

def test_app_starts():
    with flask_app.test_client() as client:
        response = client.get('/')
        assert response.status_code == 200  # Assuming your root route returns a 200 OK status

