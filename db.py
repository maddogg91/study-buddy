
import os
import pymongo
import enc
import jsonify
import uuid
from passlib.hash import pbkdf2_sha256
from flask import request
from Group import Group

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
            
 


def searchForGroupChat(keyword, criteria):
    groupChat= db["groupchat"]
    returnedGroups= []
    #finds keyword in db based off the criteria or filter. Currently set to name.
    query = { criteria: {'$regex' : keyword , '$options' : 'i'}}
    try:
        results= groupChat.find()
        for result in results:
            group= Group(result["_id"], result["name"], result["users"], result["createTimestamp"], result["description"],
            result["photo"], result["messages"])
            returnedGroups.append(group) 
        return returnedGroups
    except:
         print("Error with Group Chat search")
         return "No results found..."
      
      
def existingChats():
    groupChat= db["groupchat"]
    gc= []
    #reveals existing groupchats in database
    try:
        results= groupChat.find()
        for result in results:
            group= Group(result["_id"], result["name"], result["users"], result["createTimestamp"], result["description"],
            result["photo"], result["messages"])
            gc.append(group) 
        return gc
    except:
         print("Error with Group Chat")
         return "No results found..."