
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


def login(user, passw):
    db= connectDB() 
    collection= db["registration"]
    #user= enc.decrypt(user)
    #passw= enc.decrypt(passw)
    query = { "username" : user , "password" : passw }
    try:
        loginInfo = collection.find_one(query)
        print(loginInfo["username"])
        return True
    except:
        print("No user found, please try again.")
        return False
    
class User:   
    def signUp(self):
        db=connectDB()
            #Create user obj
        user={
            "_id":uuid.uuid4().hex,
            "username":request.form.get('name'),
            "password":request.form.get('password'),
            "email":request.form.get('email'),
            "birthday":request.form.get('birthday')
        }
        #encryption of data of password
        user['password']=pbkdf2_sha256.encrypt(user['password'])
        if db.users.find_one({"email":user['email']}):
            return jsonify({"error":"email already in use"}),400
        db.users.insert_one(user)

        return jsonify(user),200