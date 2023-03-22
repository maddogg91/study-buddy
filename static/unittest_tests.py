import unittest # Default python library for unit testing
from passlib.hash import pbkdf2_sha256
from unittest.mock import MagicMock # allows a mock of the database
from pymongo import MongoClient # the actual database

class Test(unittest.TestCase):
    #unmocked unit test for password encryption used for encrypting user passwords 

    def test_pbkdf2_sha256(self):
        # testing reveal password
        passw = "123"
        encrypted_password = pbkdf2_sha256.hash(passw)
        self.assertTrue(pbkdf2_sha256.verify(passw, encrypted_password))

        # another password test to see hash
        other_password = "543"
        self.assertFalse(pbkdf2_sha256.verify(other_password, encrypted_password))


# Groupchat user input doc for groupchat photo upload to database
# User must have a png file or a jpeg file 

def is_requiredphoto(doc):
    for key, value in doc.items():
        if key == "photo":
            if value.lower().endswith(".png") or value.lower().endswith(".jpeg"):
                return True
            else: 
                return False

class TestGroupInput(unittest.TestCase):
        
    #creating test document from groupchat schema for assertions
    def testDoc(self):
        #mock doc with correct jpeg or png
        mock_doc = {
            "_id": "63ed9884d30a9322054",
            "users": [],
            "name": "SUPER ICHIGO FANCLUB",
            "description": "RAWR Ichigo",
            "photo": "main-qimg-4beb7e63ca851119d172f8fd665f5fd5.jpeg",
            "createTimestamp": "2023-02-15T21:44:20.835+00:00",
            "messages": [] }
    
        self.assertTrue(is_requiredphoto(mock_doc))
        
        #mock doc with wrong picture file name
        mock_doc = {
            "_id": "63ed9884d30a9322054",
            "users": [],
            "name": "SUPER ICHIGO FANCLUB",
            "description": "RAWR Ichigo",
            "photo": "main-qimg-4beb7e63ca851119d172f8fd665f5fd5.jfif",
            "createTimestamp": "2023-02-15T21:44:20.835+00:00",
            "messages": [] }
        
        self.assertFalse(is_requiredphoto(mock_doc))   
    

if __name__ == "__main__":
    # You can run this file using:   python unittest_tests.py
    unittest.main()