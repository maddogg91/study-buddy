import pytest
import sys
import os
import requests


directory = os.path.dirname(os.path.realpath(__file__))

parent = os.path.dirname(directory)

sys.path.append(parent)

from main import create_app

def test_index():
    response= requests.get('http://127.0.0.1:5000')
    assert response.status_code == 200
    

def test_login():
    response= requests.post("http://127.0.0.1:5000/login", data= {
        "user": "TestUser1",
        "password": "ABCDEFG"
        })
    assert response.status_code == 200    