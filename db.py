import pymongo

def connectDB():
    client = pymongo.MongoClient("mongodb+srv://studybuddy:OctG2CDRxy05yzOf@cluster0.4grai.mongodb.net/?retryWrites=true&w=majority")
    db = client["studybuddy"]
    return db


def login(user, passw):
    db= connectDB() 
    collection= db["registration"]
    query = { "username" : user , "password" : passw }
    try:
        loginInfo = collection.find_one(query)
        print(loginInfo["username"])
        return True
    except:
        print("No user found, please try again.")
        return False
    
    
    
