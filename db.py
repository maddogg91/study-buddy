
import os
import pymongo
import enc
import jsonify
import uuid
from passlib.hash import pbkdf2_sha256
from flask import request
import logging
logging.basicConfig(filename='logging1.txt', level=logging.DEBUG)


def connectDB():
    with open('keys/db.txt', 'rb') as p:
        conn = p.read()
    client = pymongo.MongoClient(enc.decrypt(conn))
    db = client["studybuddy"]
    return db


def login(user, passw):
    db= connectDB() 
    collection= db["users"]
    #user= enc.decrypt(user)
    #passw= enc.decrypt(passw)
    query = { "username" : user }
    try:
        loginInfo = collection.find_one(query)
        pbkdf2_sha256.verify(passw, loginInfo["password"])
        return True
    except:
        print("No user found, please try again.")
        return False
def groups():
    db=connectDB()
    cursor= db["groupchat"]
    gc1=cursor.find().toArray()
    db.logger.debug("debug log info")
    #num=existing_groupchat.find().count()
    #category _id
    #
    return gc1
class User:   
    def signUp(self):
        db=connectDB()
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
            #return jsonify(user),200
            return True

        #return jsonify({"error:Signup failed"}),400