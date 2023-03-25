import os
import unittest
import pymongo
import enc
import uuid
from passlib.hash import pbkdf2_sha256
from flask import request
from Group import Group
import datetime
from bson.objectid import ObjectId
import json
from groupmsg import groupmsg

def connectDB():
    client = pymongo.MongoClient("mongodb+srv://studybuddy:OctG2CDRxy05yzOf@cluster0.4grai.mongodb.net/?retryWrites=true&w=majority")
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
                # replace the user's information in the database
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
    def googlesettingsInfo(self,id):
        
        collection=db['googleUsers']
        new_username=request.form['new_username']
        new_bday=request.form['new_bday']
        # get the user's ID from the google users session

        user = collection.find_one({'_id': id})
                # update the user's information in the database
        collection.update_one(
                        {'_id': id},
                        {"$set":{
                            'username':new_username,
                            'birthday':new_bday
                        }
                        }                            
            )
        return True
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
        return col.find(query)

def get_users():
    return db.users.find()
 
def searchUsers(keyword, criteria):
    foundUsers= []
    profiles= []
    try:
        results= search(keyword, criteria, "users")
      
        for result in results:
            print(result["_id"])
            profile= db.profile.find_one({"userId": result["_id"]})
            foundUsers.append(result)
            print(profile)
            primary_info= {
                "name" : profile["fname"] + " " + profile["lname"], 
                "photo" : profile["profilepic"],
                "description": profile["bio"]
            }
            profiles.append(primary_info)
        return foundUsers, profiles
    except:
         print("Error with users search")
         return "No results found...", ""

def createChat(data, file, _id):
    groupDB = db["groupchat"]
    newUser = []
    user= {"id": _id, "permissionType": "admin"}
    newUser.append(user)
    newChat= {

        "users": newUser,
        "name": data.form.get("groupName"),
        "description": data.form.get("groupDescription"),
        "photo": file.filename,
        "createTimestamp": datetime.datetime.now(),
        "messages": []
    }
    return groupDB.insert_one(newChat)

def existingChats(keyword, criteria):
    returnedGroups= []
    try:
        results= search(keyword, criteria, "groupchat")
        for result in results:
            group= Group(result["_id"], result["name"], result["users"], result["createTimestamp"], result["description"],
            result["photo"], result["messages"])
            returnedGroups.append(json.loads(json.dumps(group.__dict__))) 
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
            profile= db.profile.find_one({"userId":sender["_id"]})
            if profile is None:
                userProfile(sender["_id"])
                profile= db.profile.find_one({"userId":sender["_id"]})
                
            gm= groupmsg(groupId, sender, profile["fname"], profile["lname"], timestamp, msg, profile["profilepic"])
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


def userProfile(id):
    profile= search(id, "userId", "profile")
    count= list(profile)
    user=""
    try:
        if len(count) > 0:
            for i in count:
               user= {
                    "_id": str(i["_id"]),
                     "fname": i["fname"],
                     "lname": i["lname"],
                     "major": i["major"],
                     "minor": i["minor"],
                     "status": i["status"],
                     "gender": i["gender"],
                     "profilepic": i["profilepic"],
                     "bio": i["bio"],
                     "quizAnswers": i["quizAnswers"]
                }
            return user
        else:
            user= {
                    "_id": uuid.uuid4().hex,
                     "userId": str(id),    
                     "fname": "",
                     "lname": "",
                     "major": "",
                     "minor": "",
                     "status": "",
                     "gender": "",
                     "profilepic": "defG.png",
                     "bio": "",
                     "quizAnswers": ""
            }
            db.profile.insert_one(user)
            user._id = str(user._id)
            return user
    except Exception as e:
        print(e)
        return user
   
def saveUserProfile(_id, req):
        print(_id)
        data= search(_id, "userId", "profile")
        profile= list(data)
        profile= profile[0]
        for i in req.form:
            if(req.form[i]== ""):
                print("No change for " + i)
            else:
                profile[i]= req.form[i]
        try:
            if(req.files["profilepic"].filename== ""):
                print("No change for Profile Pic")
                
            else:
                profile["profilepic"]= req.files["profilepic"].filename
        except:
            print("No update needed for profile photo")
        db.profile.replace_one({"userId": _id}, profile)

def loadQuizAnswers(_id):
    data= search(_id, "userId", "profile")
    profile= list(data)
    profile= profile[0]
    return profile["quizAnswers"]
    
def saveMessage(data, _id):
   
    messageId= str(uuid.uuid4().hex)
    
    message= {
                "_id": ObjectId(messageId[:24]),
                "sender": _id,
                "createTimestamp": datetime.datetime.now(),
                "message": data["message"]
    }
    db.messages.insert_one(message)
    groupchat= db.groupchat.find_one({"_id": ObjectId(data["group"])})
    groupchat["messages"][0].append(str(message["_id"]))
    db.groupchat.replace_one({"_id": ObjectId(data["group"])}, groupchat)
    
def joingroup(gid, uid):
    groupchat= db.groupchat.find_one({"_id": ObjectId(gid)})
    user = {
            "id": uid,
            "permissionType": "user"
    }
    groupchat["users"].append(user)
    db.groupchat.replace_one({"_id": ObjectId(gid)}, groupchat)

