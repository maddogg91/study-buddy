import pytest
import sys
import os
import requests

def test_index():
    response= requests.get('http://127.0.0.1:5000')
    assert response.status_code == 200
    

def test_login():
    response= requests.post("http://127.0.0.1:5000/login", data= {
        "user": "TestUser1",
        "password": "ABCDEFG"
        })
    assert response.status_code == 200    
