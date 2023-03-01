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
from groupmsg import groupmsg

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
class Change:
    def changeInfo(self,id):
        collection=db['users']
        # get the user's current password and new password from the form data
        current_password = request.form['current_password']
        new_password = request.form['new_password']
        new_email=request.form['new_email']
        new_username=request.form['new_username']
        new_bday=request.form['new_bday']
        # get the user's ID from the session

        # check if the current password is correct
        try:
            user = collection.find_one({'_id': id})
            pbkdf2_sha256.verify(current_password, user["password"])
                # update the user's information in the database
            collection.replace_one(
                        {'_id': id},
                        {
                            'username':new_username,
                            'password':pbkdf2_sha256.encrypt(new_password),
                            'email':new_email,
                            'birthday':new_bday
                        }                            
            )
            return True
        except:
            return("Password Wrong, Please enter correct password to update information")
    def changeGoogleinfo(self,id):
        collection=db['googleUsers']
        # get the user's current password and new password from the form data
        current_password = request.form['current_password']
        new_username=request.form['new_username']
        new_bday=request.form['new_bday']
        # get the user's ID from the session

        # check if the current password is correct
        try:
            user = collection.find_one({'_id': id})
            pbkdf2_sha256.verify(current_password, user["password"])
                # update the user's information in the database
            collection.insert(
                        {'_id': id},
                        {
                            'username':new_username,
                            'birthday':new_bday,
                        })
            return True
        except:
            return("Password Wrong, Please enter correct password to update information")
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
        db.googleUsers.insert_one(query)
        google= db.googleUsers.find_one({"email": email})
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
    messages= []
    results= []
    try:
        _id= ObjectId(groupId)
        query= {"_id" : _id }
        #Searches group chat db for groupchat with specified id.
        group= db.groupchat.find_one(query)
        #Grabs messages Array 
        groupMessages= group['messages'][0]
        #For each message in messages, create results list
        for m in groupMessages:
            results.append(db.messages.find_one(ObjectId(m)))
            
        #Each result create group message object which includes groupid, sender, timestamp, and message
        for result in results:
           
            timestamp= result["createTimestamp"]
            msg = result["message"]
            sender= db.users.find_one(result["sender"])
            if sender is not None:
                fromsender = sender["username"]
            else:
                sender= db.googleUsers.find_one(result["sender"])
                fromsender = sender["email"]
            
            gm= groupmsg(groupId, sender, timestamp, msg)
            messages.append(json.loads(json.dumps(gm.__dict__)))
            
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
        returnedGroups.append(json.loads(json.dumps(group.__dict__)))
   
    return returnedGroups

         
