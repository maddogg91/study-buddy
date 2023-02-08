
import pymongo
import enc
import jsonify
import uuid
from passlib.hash import pbkdf2_sha256
from flask import request




def connectDB():
    with open('keys/db.txt', 'rb') as p:
        conn = p.read()
    client = pymongo.MongoClient(enc.decrypt(conn))
    db = client["studybuddy"]
    return db

db= connectDB()

def login(user, passw):
    collection= db["users"]
    query = { "username" : user }
    try:
        loginInfo = collection.find_one(query)
        pbkdf2_sha256.verify(passw, loginInfo["password"])
        return loginInfo
    except:
        print("No user found, please try again.")
        return False
    
class User:   
    def signUp(self):
            #Create user obj for submitted fields
        user={
            "_id":uuid.uuid4().hex,
            "username":request.form.get('name'),
            "password":request.form.get('password'),
            "email":request.form.get('email'),
            "birthday":request.form.get('birthday')
        }
        #encryption of data of password
        user['password']=pbkdf2_sha256.encrypt(user['password'])
        #if user already signed up with error address they will have error
        if db.users.find_one({"email":user['email']}):
           return False
        if db.users.insert_one(user):
            return True
            
    # def lookUp(self):
        # db.users.find_one
# class Group:
    # def createGroup(self):
    # user= db["users"]
    
    
    # group = {
            # "_id": uuid.uuid4().hex,
            # "users": [
                # "user" : 
            # ]
    
    # }
    
        

        