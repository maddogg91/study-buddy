# Study Buddy
## Study Buddy is designed to coordinate users together to meet study needs. ##
This web application functions as an engine in which users can create a groupchat and update profile information using Python Flask
## Services needed to run the web application : contact developers ##
  * ***Mongo DB is used and encyption files are needed***
    * Pymongo is used refer to link for further information https://www.mongodb.com/docs/drivers/pymongo/
    *Mongo DB Compass is used to visualize and view our data tables : https://www.mongodb.com/products/compass

  * ***Google Oauth is used to sign users in***
    * https://developers.google.com/identity/protocols/oauth2
  * Requirements.txt is applied so no pip install is needed from your end

## Product video
https://www.youtube.com/watch?v=4rvgY-5Tog8
 
## MVP Methods and  Description ##
MVP Tasks  | Description 
------------- | ------------- 
Non Google user Sign Up  | User will sign up with email password birthday and username.Then User information is stored into Users table in mongoDB | 
Google user Sign Up | User who signs up with Google will be rerouted to the google login page and will then have their email and a unique id | 
Change User information  | Google Users and Non google Users will be rerouted to different pages with different permissions to update specific data. Using mongo db update and inset commands to update user database information
Create Group | User can create group descriptions, add groupchat photo, and name and it will be inserted into groupchat collection in mongoDB
Join Group | User can search for groups to join and opt in or out and their unique id will be added to groupchat collection in Mongo DB 
Groupchat + Chat feautures | User can Post a text message and it will be added into messages collection in Mongo DB and be outputted in a boostrap styled text bubble of real time timestamps from newest to oldest  messages 
Match Making Quiz | Allows a user to take a compatability quiz and match with similar studiers from 5 stars (best match) to 1 star (worst match) 

# Signup
![](https://github.com/maddogg91/study-buddy/google_signin.gif)
# Profile Settings
![](https://github.com/maddogg91/study-buddy/profile_settings.gif)
# Join a group
![](https://github.com/maddogg91/study-buddy/join_group.gif)
# Message in chat
![](https://github.com/maddogg91/study-buddy/chat_message.gif)
# Matchmaking quiz
 ![](https://github.com/maddogg91/study-buddy/match_quiz.gif)

## Stretch goals for the future ##
* Google Calendar API
* Matching algorithm for study buddy quiz 
* Profile section 
