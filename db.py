import os
import pymongo
import enc
import jsonify
import uuid
from passlib.hash import pbkdf2_sha256
from flask import request
from Group import Group
import datetime
from bson.objectid import ObjectId
import json
import base64

def connectDB():
    with open('keys/db.txt', 'rb') as p:
        conn = p.read()
    client = pymongo.MongoClient(enc.decrypt(conn))
    db = client["studybuddy"]
    return db

db = connectDB()

def login(user, passw):
    collection= db["users"]
    if "@" not in user: 
        query = { "username" : user }
    else:
        query = { "email" : user }
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

def googleSignup(email):
    google= db.googleUsers.find_one({"email": email})
    if google is not None:
        return google
    else:
        query= {"_id": uuid.uuid4().hex ,"email" : email}
        google= db.googleUsers.insert_one(query)
        return google
    
def search(keyword, criteria, collection):
    #selects col or collection based off collection var
    col= db[collection]
    if(keyword=="" or criteria==""):
        
        #return all results
        return col.find()
    else:
        #return specified results
        query = { criteria: {'$regex' : keyword , '$options' : 'i'}}
        #print(query)
        return col.find(query)
    
def searchUsers(keyword, criteria):
    foundUsers= []
    try:
        results= search(keyword, criteria, "users")
        #print(results)
        for result in results:
            
            foundUsers.append(result) 
        return foundUsers
    except:
         print("Error with users search")
         return "No results found..."

def createChat(data, file):
    groupDB = db["groupchat"]
    newChat= {

        "users": "admin",
        "name": data.form.get("groupName"),
        "description": data.form.get("groupDescription"),
        "photo": file.filename,
        "createTimestamp": datetime.datetime.now(),
        "messages": ""
    }
    return groupDB.insert_one(newChat)

def existingChats(keyword, criteria):
    returnedGroups= []
    try:
        results= search(keyword, criteria, "groupchat")
        for result in results:
            group= Group(result["_id"], result["name"], result["users"], result["createTimestamp"], result["description"],
            result["photo"], result["messages"])
            returnedGroups.append(group) 
        return returnedGroups
    except:
         print("Error with Group Chat search")
         return "No results found..."
         
def savequiz(data, user):
    coll= db["profile"]
    answers= []
    for i in data:
        answers.append(data[i])
    profile= db.profile.find_one({"userId": user})
   
    if(profile!= ""):
       profile["quizAnswers"]= answers

       coll.replace_one({"userId":profile["userId"]}, profile)
       return answers
    else:
        db.profile.insert({"userId": user, "quizAnswers": answers})
        return answers
        
        
def loadGroupMessages(groupId):
    message = { "sender" : "", "timestamp" : "", "message" : ""}
    messages= []
    results= []
    try:
        _id= ObjectId(groupId)
        query= {"_id" : _id }
        group= db.groupchat.find_one(query)
        groupMessages= group['messages'][0]
        for m in groupMessages:
            results.append(db.messages.find_one(ObjectId(m)))
            print(m)
            
        for result in results:
            sender= db.users.find_one(result["sender"])
            if sender is not None:
                message["sender"] = sender["username"]
            else:
                sender= db.googleUsers.find_one(result["sender"])
                message["sender"] = sender["email"]
            message["timestamp"]= result["createTimestamp"]
            message["message"] = result["message"]
            print(message)
            messages.append(message)
        return messages
   
    except Exception as e:
        print(e)
        print("No messages found")
    
def userChats(username):
    returnedGroups= []
    userchats= db.groupchat.find({"users.id": username})
    for result in userchats:
        group= Group(result["_id"], result["name"], result["users"], result["createTimestamp"], result["description"],
            result["photo"], result["messages"])
        returnedGroups.append(json.dumps(group.__dict__))
    print(returnedGroups)
    return returnedGroups
         
    

