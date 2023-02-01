import pymongo
import enc




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
    
    
    
