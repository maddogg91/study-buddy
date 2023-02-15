
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
      