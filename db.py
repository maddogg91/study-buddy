"""load modules"""
import json
import uuid
import datetime
from bson.objectid import ObjectId
import pymongo
from passlib.hash import pbkdf2_sha256
from flask import request
import enc
from Group import Group
from groupmsg import groupmsg

def connect_db():
    """connect to db"""
    with open('keys/db.txt', 'rb') as reader:
        conn = reader.read()
    client = pymongo.MongoClient(enc.decrypt(conn))
    db_studybuddy = client["studybuddy"]
    return db_studybuddy

db_connection = connect_db()

def login(user, passw):
    """attempts login"""
    collection= db_connection["users"]
    if "@" not in user:
        query = { "username" : user }
    else:
        query = { "email" : user }
    try:
        login_info = collection.find_one(query)
        pbkdf2_sha256.verify(passw, login_info["password"])
        return login_info

    except: # pylint: disable=bare-except
        print("No user found, please try again.")
        return False

class Change:
    """Change class"""
    def change_info(self,_id):
        """attempts change info"""
        collection=db_connection['users']
        # get the user's current password and new password from the form data
        current_password = request.form['current_password']
        new_password = request.form['new_password']
        new_email=request.form['new_email']
        new_username=request.form['new_username']
        new_bday=request.form['new_bday']
        # get the user's ID from the session

        # check if the current password is correct
        try:
            user = collection.find_one({'_id': _id})
            pbkdf2_sha256.verify(current_password, user["password"])
                # replace the user's information in the database
            collection.replace_one(
                        {'_id': _id},
                        {
                            'username':new_username,
                            'password':pbkdf2_sha256.encrypt(new_password),
                            'email':new_email,
                            'birthday':new_bday
                        }
            )
            return True
        except: # pylint: disable=bare-except
            return "Password Wrong, Please enter correct password to update information"
    def googlesettingsinfo(self,_id):
        """google settings"""
        collection=db_connection['googleUsers']
        new_username=request.form['new_username']
        new_bday=request.form['new_bday']
        # get the user's ID from the google users session
        collection.find_one({'_id': _id})
                # update the user's information in the database
        collection.update_one(
                        {'_id': _id},
                        {"$set":{
                            'username':new_username,
                            'birthday':new_bday
                        }
                        }
            )
        return True
class User: # pylint: disable=R0903
    """User class"""
    def signup(self): # pylint: disable=R1710
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
        if db_connection.users.find_one({"email":user['email']}):
            return False, db_connection.users.find_one({"email":user['email']})
        if db_connection.users.insert_one(user):
            return True, db_connection.users.find_one({"email":user['email']})

def googlesignup(email):
    """attempts google signup"""
    google= db_connection.googleUsers.find_one({"email": email})
    if google is not None:
        return google
    query= {"_id": uuid.uuid4().hex ,"email" : email}
    db_connection.googleUsers.insert_one(query)
    google= db_connection.googleUsers.find_one({"email": email})
    return google

def search(keyword, criteria, collection):
    """Search collection"""
    #selects col or collection based off collection var
    col= db_connection[collection]
    if(keyword=="" or criteria==""):
        #return all results
        return col.find()
    query = { criteria: {'$regex' : keyword , '$options' : 'i'}}
    return col.find(query)

def get_users():
    """get_users"""
    return db_connection.users.find()

def get_google():
    """returns all google_users"""
    return list(db_connection.googleUsers.find())

def searchusers(keyword, criteria):
    """searchusers"""
    foundusers= []
    profiles= []
    try:
        results= search(keyword, criteria, "users")

        for result in results:
            profile= db_connection.profile.find_one({"userId": result["_id"]})
            foundusers.append(result)
            primary_info= {
                "name" : profile["fname"] + " " + profile["lname"], 
                "photo" : profile["profilepic"],
                "description": profile["bio"]
            }
            profiles.append(primary_info)
        return foundusers, profiles
    except: # pylint: disable=bare-except
        print("Error with users search")
        return "No results found...", ""

def createchat(data, file, _id):
    """createchat"""
    groupdb = db_connection["groupchat"]
    newuser = []
    group_users= data.form.get("groupUsers")
    if len(group_users) > 0:
        users_by_id= rip_email(group_users)
        for _uid in users_by_id:
            _user= {"id": _uid, "permissionType": "user"}
            newuser.append(_user)
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
    except: # pylint: disable=bare-except
        print("Error with Group Chat search")
        return "No results found..."

def savequiz(data, user):
    """savequiz"""
    coll= db_connection["profile"]
    answers= []
    for i in data:
        answers.append(data[i])
    profile= db_connection.profile.find_one({"userId": user})

    if profile != "":
        profile["quizAnswers"]= answers
        coll.replace_one({"userId":profile["userId"]}, profile)
        return answers
    db_connection.profile.insert({"userId": user, "quizAnswers": answers})
    return answers


def loadgroupmessages(group_id): # pylint: disable=R0914, R1710
    """loadgroupmessages"""
    messages= []
    results= []
    try:
        _id= ObjectId(group_id)

        query= {"_id" : _id }
        #Searches group chat db for groupchat with specified id.
        group= db_connection.groupchat.find_one(query)
        #Grabs messages Array
        group_messages= group['messages'][0]
        #For each message in messages, create results list
        for found_message in group_messages:
            results.append(db_connection.messages.find_one(ObjectId(found_message)))

        #Each result create group message object which
        #includes groupid, sender, timestamp, and message
        for result in results:

            timestamp= result["createTimestamp"]
            msg = result["message"]
            sender= db_connection.users.find_one(result["sender"])
            if sender is None:
                sender= db_connection.googleUsers.find_one(result["sender"])
            profile= db_connection.profile.find_one({"userId":sender["_id"]})
            if profile is None:
                user_profile(sender["_id"])
                profile= db_connection.profile.find_one({"userId":sender["_id"]})
            group_message= groupmsg(group_id, sender, profile["fname"], profile["lname"],
            timestamp, msg, profile["profilepic"])
            messages.append(json.loads(json.dumps(group_message.__dict__)))
        return messages

    except Exception as exeption: # pylint: disable=bare-except, broad-exception-caught
        print(exeption)
        print("No messages found")

def messages_by_time(timestamp, group_id):
    """messages by time"""
    messages_sort= []
    messages= loadgroupmessages(group_id)
    print("attempting to update")
    for message in messages:
        #Checks timestamp of the messages and removes older messages
        msg_ts= datetime.datetime.strptime(message["timestamp"],'%Y-%m-%d %H:%M:%S')
        if timestamp < msg_ts.timestamp():
            messages_sort.append(message)
    print(messages_sort)
    return messages_sort

def userchats(username):
    """userchats"""
    returned_groups= []
    user_chats= db_connection.groupchat.find({"users.id": username})
    for result in user_chats:
        group= Group(result["_id"], result["name"], result["users"],
        result["createTimestamp"], result["description"],
            result["photo"], result["messages"])
        returned_groups.append(json.loads(json.dumps(group.__dict__)))
    return returned_groups


def user_profile(_id):
    """userprofile"""
    profile= search(_id, "userId", "profile")
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
        user= {
                "_id": uuid.uuid4().hex,
                 "userId": str(_id),    
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
        db_connection.profile.insert_one(user)
        return user
    except Exception as exeption: # pylint: disable=bare-except, broad-exception-caught
        print(exeption)
        return user

def saveuserprofile(_id, req):
    """saveuserprofile"""
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
    except: # pylint: disable=bare-except
        print("No update needed for profile photo")
    db_connection.profile.replace_one({"userId": _id}, profile)

def loadquizanswers(_id):
    """loadquizanswers"""
    data= search(_id, "userId", "profile")
    profile= list(data)
    profile= profile[0]
    return profile["quizAnswers"]

def savemessage(data, _id):
    """save messages"""
    message_id= str(uuid.uuid4().hex)
    response= []
    time= datetime.datetime.now()
    time= time.strftime("%Y-%m-%d %H:%M:%S")
    message= {
                "_id": ObjectId(message_id[:24]),
                "sender": _id,
                "createTimestamp": time,
                "message": data["message"]
    }
    db_connection.messages.insert_one(message)
    groupchat= db_connection.groupchat.find_one({"_id": ObjectId(data["group"])})
    groupchat["messages"][0].append(str(message["_id"]))
    db_connection.groupchat.replace_one({"_id": ObjectId(data["group"])}, groupchat)
    user_message= loadgroupmessages(str(groupchat["_id"]))
    for filter_message in user_message:
        if filter_message["message"] == data["message"]:
            print("match!")
            response.append(filter_message)
    return response

def joingroup(gid, uid):
    """joingroup"""
    groupchat= db_connection.groupchat.find_one({"_id": ObjectId(gid)})
    user = {
            "id": uid,
            "permissionType": "user"
    }
    groupchat["users"].append(user)
    db_connection.groupchat.replace_one({"_id": ObjectId(gid)}, groupchat)

def rip_email(data):
    """rips email from data query"""
    users= data.split(",")
    user_list= []
    for user in users:
        print(user.split(":::")[0])
        email= db_connection.users.find_one({"username": user.split(":::")[0]})
        if email is None:
            email= db_connection.googleUsers.find_one({"email": user.split(":::")[1]})
        user_list.append(email["_id"])
    return user_list

def loadgroupchat(gid):
    """loads current instance of group chat called"""
    group_chat= db_connection.groupchat.find_one(gid)
    group_chat["_id"]= str(group_chat["_id"])
    return group_chat

def buddy_search(uid):
    """db function to find buddies based on matchmaking quiz"""
    users_perfect= []
    users_4stars= []
    users_3stars= []
    users_2stars= []
    users_1star= []
    percentage= 0
    profile= user_profile(uid)
    alluser_profile= list(db_connection.profile.find())
    for user in alluser_profile:
        user["_id"]= str(user["_id"])
        percentage= 0
        if user["quizAnswers"] != "":
            for i in range(0, 10):
                if user["quizAnswers"][i] is profile["quizAnswers"][i]:
                    percentage = percentage + 10
            if percentage > 81:
                if user["userId"]!= uid:
                    users_perfect.append(user)
            elif 69 < percentage < 81:
                users_4stars.append(user)
            elif 49 < percentage < 61:
                users_3stars.append(user)
            elif 29 < percentage < 41:
                users_2stars.append(user)
            else:
                users_1star.append(user)
    buddy_data= {
    "best": users_perfect,
    "second": users_4stars,
    "third": users_3stars,
    "fourth": users_2stars,
    "last": users_1star
    }
    return buddy_data