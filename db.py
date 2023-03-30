"""load modules"""
import json
from bson.objectid import ObjectId
import pymongo
import uuid
from passlib.hash import pbkdf2_sha256
import datetime
from flask import request
import enc
from Group import Group
from groupmsg import groupmsg

def connect_db():
    """connect to db"""
    with open('keys/db.txt', 'rb') as p:
        conn = p.read()
    client = pymongo.MongoClient(enc.decrypt(conn))
    db = client["studybuddy"]
    return db

db = connect_db()

def login(user, passw):
    """attempts login"""
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
    """Change class"""
    def change_info(self,id):
        """attempts change info"""
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
            return "Password Wrong, Please enter correct password to update information"
    def googlesettingsinfo(self,id):
        """google settings"""
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
    """User class"""
    def signup(self):
        """attempts signup"""
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
            return False, db.users.find_one({"email":user['email']})
        if db.users.insert_one(user):
            return True, db.users.find_one({"email":user['email']})

def googlesignup(email):
    """attempts google signup"""
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
    """get_users"""
    return db.users.find()

def searchusers(keyword, criteria):
    """searchusers"""
    foundusers= []
    profiles= []
    try:
        results= search(keyword, criteria, "users")

        for result in results:
            print(result["_id"])
            profile= db.profile.find_one({"userId": result["_id"]})
            foundusers.append(result)
            print(profile)
            primary_info= {
                "name" : profile["fname"] + " " + profile["lname"], 
                "photo" : profile["profilepic"],
                "description": profile["bio"]
            }
            profiles.append(primary_info)
        return foundusers, profiles
    except:
        print("Error with users search")
        return "No results found...", ""

def createchat(data, file, _id):
    """createchat"""
    groupdb = db["groupchat"]
    newuser = []
    user= {"id": _id, "permissionType": "admin"}
    newuser.append(user)
    newchat= {

        "users": newuser,
        "name": data.form.get("groupName"),
        "description": data.form.get("groupDescription"),
        "photo": file.filename,
        "createTimestamp": datetime.datetime.now(),
        #Creates default message
        "messages": [["641df8d9b1292a0a0e1c2781"]]
    }
    return groupdb.insert_one(newchat)

def existingchats(keyword, criteria):
    """existingchats"""
    returnedgroups= []
    try:
        results= search(keyword, criteria, "groupchat")
        for result in results:
            group= Group(result["_id"], result["name"], result["users"],
            result["createTimestamp"], result["description"],
            result["photo"], result["messages"])
            returnedgroups.append(json.loads(json.dumps(group.__dict__)))
        return returnedgroups
    except:
        print("Error with Group Chat search")
        return "No results found..."

def savequiz(data, user):
    """savequiz"""
    coll= db["profile"]
    answers= []
    for i in data:
        answers.append(data[i])
    profile= db.profile.find_one({"userId": user})

    if profile != "":
        profile["quizAnswers"]= answers
        coll.replace_one({"userId":profile["userId"]}, profile)
        return answers
    db.profile.insert({"userId": user, "quizAnswers": answers})
    return answers


def loadgroupmessages(groupId):
    """loadgroupmessages"""
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

        #Each result create group message object which
        #includes groupid, sender, timestamp, and message
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

            gm= groupmsg(groupId, sender, profile["fname"], profile["lname"],
            timestamp, msg, profile["profilepic"])
            messages.append(json.loads(json.dumps(gm.__dict__)))
        return messages

    except Exception as e:
        print(e)
        print("No messages found")

def messages_by_time(timestamp, group_id):
    """messages by time"""
    messages_sort= []
    messages= loadgroupmessages(group_id)
    print("attempting to update")
    for message in messages:
        #Checks timestamp of the messages and removes older messages
        msg_ts= datetime.datetime.strptime(message["timestamp"],'%Y-%m-%d %H:%M:%S')
        if timestamp <= msg_ts.timestamp():
            messages_sort.append(message)
    print(messages_sort)        
    return messages_sort

def userchats(username):
    """userchats"""
    returnedGroups= []
    userchats= db.groupchat.find({"users.id": username})
    for result in userchats:
        group= Group(result["_id"], result["name"], result["users"],
        result["createTimestamp"], result["description"],
            result["photo"], result["messages"])
        returnedGroups.append(json.loads(json.dumps(group.__dict__)))

    return returnedGroups


def userprofile(id):
    """userprofile"""
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

def saveuserprofile(_id, req):
    """saveuserprofile"""
    print(_id)
    data= search(_id, "userId", "profile")
    profile= list(data)
    profile= profile[0]
    for i in req.form:
        if req.form[i] == "":
            print("No change for " + i)
        else:
            profile[i]= req.form[i]
    try:
        if req.files["profilepic"].filename == "":
            print("No change for Profile Pic")

        else:
            profile["profilepic"]= req.files["profilepic"].filename
    except:
        print("No update needed for profile photo")
    db.profile.replace_one({"userId": _id}, profile)

def loadquizanswers(_id):
    """loadquizanswers"""
    data= search(_id, "userId", "profile")
    profile= list(data)
    profile= profile[0]
    return profile["quizAnswers"]

def savemessage(data, _id):
    """save messages"""
    messageId= str(uuid.uuid4().hex)
    response= []
    time= datetime.datetime.now()
    time= time.strftime("%Y-%m-%d %H:%M:%S")
    message= {
                "_id": ObjectId(messageId[:24]),
                "sender": _id,
                "createTimestamp": time,
                "message": data["message"]
    }
    db.messages.insert_one(message)
    groupchat= db.groupchat.find_one({"_id": ObjectId(data["group"])})
    groupchat["messages"][0].append(str(message["_id"]))
    db.groupchat.replace_one({"_id": ObjectId(data["group"])}, groupchat)
    user_message= loadgroupmessages(str(groupchat["_id"]))
    for filter_message in user_message:
        if filter_message["message"] == data["message"]:
            print("match!")
            response.append(filter_message)
    return response

def joingroup(gid, uid):
    """joingroup"""
    groupchat= db.groupchat.find_one({"_id": ObjectId(gid)})
    user = {
            "id": uid,
            "permissionType": "user"
    }
    groupchat["users"].append(user)
    db.groupchat.replace_one({"_id": ObjectId(gid)}, groupchat)
    
# def test(message):
    # msg_ts= datetime.datetime.strptime(message,'%Y-%m-%d %H:%M:%S' )
    # print(msg_ts.timestamp())
    

# test("2023-02-21 05:00:00")