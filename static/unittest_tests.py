import unittest # Default python library for unit testing
from passlib.hash import pbkdf2_sha256

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
    #regardless of order of keys testing if dict are equal
    def test_dict(self):
        expected = {'c': 4, 'd': 7}
        actual = {'d': 7, 'c': 4}
        self.assertDictEqual(expected, actual)
   


if __name__ == "__main__":
    # You can run this file using:   python unittest_tests.py
    unittest.main()