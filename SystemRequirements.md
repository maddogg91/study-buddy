## **1.1 Purpose**

The purpose of this document is to describe the implementation details
and objectives of our upcoming app, Study Buddy.

## **1.2 Intended Audience**

The intended audience for this document will be students and/or
instructors in need of study partners, homework help, etc.

## **1.3 Intended Use**

The intended use of this document is to give details, required features,
the technical design, and user features etc of SB.

## **1.4 Scope**


Study buddy is a web application that individuals can use to find study groups with students from similar classes or backgrounds. The service will provide a platform for group chats to communicate study materials and course-related materials with one another and connect to the user's calendar availability to meet to study as a group. Also, a matchmaking quiz can be shared virtually and attempted by the user to find the user's best fit as a study buddy. 
Many web applications are on the market to provide similar services for individuals like this, but Study Buddy will focus on being a relevant free platform for anyone. 


## **1.5 Definitions and Acronyms**

The remainder of the document will use the following conventions:

-   SB: Study Buddy

-   SG: Study Group

In addition:

-   \"Studier" will refer to users who have created an account

-   "Scholar" will refer to a user who creates a study group chat

# **2. Overall Description**

## **2.1 User Needs**

SB attempts to solve two core user problems:

1.  Resources provided to students can be challenging, and often
    daunting when attempting to study, but with our app's
    matchmaking implementation, a studier will be able to pair with
    other studiers in order to find the best suited study buddy for
    their requirements.

2.  There exist other platforms such as GroupMe and Discord but SB will
    be singularly focused on coordinating group discussions for
    scholastic-based endeavors directly suited to their individual
    needs.

In essence both core issues will be streamlined into a query-based,
matchmaking alignment system to appropriately link studier together.
Scholars can create SG's and invite, manage, and properly theme their
group to fit the needs of the intended course, assignment, or project.

## **2.2 Assumptions and Dependencies**
This app makes 3 major assumptions:
1. Most students tend to do well in their academics when they study with another student, this is where SG comes in to make such students meet their demand.
2. Notifications from phones, computers and other websites are a big distraction as far as studying is concerned.We will limit these distractions by restricting   notification and also locking screens during studies
3. Being able to message, video chat with each other while studying makes it more fun and interactive.  
 
Other major dependencies:
1. Our intent is to use web services and Google API’s to create design elements such as our calendar feature

# **3. System Features and Requirements**

## **3.1 Functional Requirements**

### **3.1.1 Functional Requirement 1: Login and Signup**
Description: A studier should be able to sign up for an account using their existing email. They should be required to create an account with a password and enter it before proceeding to the app. Acceptance criteria:
- If visiting app for the first time, a modal should appear asking the user to sign up
- Modal should contain options to sign up by creating username, password, email,birthday
- Confirmation text/email should be sent to the user depending on their designated sign-in option
- Once user is confirmed, modal should transition  to fill out a matchmaking quiz to fulfill their profile criteria




### **3.1.2 Functional Requirement 2: Matchmaking Quiz** 

Description: A studier should be able to take an entry quiz with various
questions that will determine the type of studier that they are. The
feature will allow users to compare to other studiers and SGs.
Acceptance criteria:

-   After signup a user will be prompted with a screen of the quiz
    questions

-   Each question will be multiple choice that a user can click on but
    each question is mandatory to complete so that the final
    statistics can be used for new studier tags

-   Once a user clicks the finish button, they will be lead to a results
    page

-   Results page statistics will create different tags that will be
    featured on a user's profile so that other user's can see what
    type of studier that they are

-   Each tag on a studiers profile can be clicked which will show a
    short description of why they are this type of learner

-   Matchmaking tags will be used for studiers to find SG that have
    similar studiers to the user when they search for a specific group

### **3.1.3 Functional Requirement 3: Group Chats**

Description: A scholar should be able to create group chats, also
referred to as Study Groups, with a name, description, and privacy
settings. Studiers should have the ability to accept invites, decline
invites, leave groups, set availability on a calendar.

-   SG contents should be accessible only to studiers who've joined the
    SG, through the set requirement of the scholar whether
    open-invitation (meaning studiers can join freely without
    approval) or closed-invitation (studiers will need a link from a
    scholar to join).

-   SG name and descriptions can be viewed after completing a
    matchmaking quiz, if public but if private the SG should only
    appear visible to invited users.

-   Invites should be sent via timed links that should expire at a given
    time.

-   SG results should prioritize SG's using matchmaking tags primarily,
    and similar terms as a secondary means.

-   Calendars should be added to each SG to ensure studiers can fill out
    their availability for particular study activities.

-   Scholars should be able to add events, reminders to calendars.

-   Scholars should have the ability to remove studiers, and moderate SG
    they've created to prevent unruly behavior. As well as delete SG,
    promote studiers to scholars in the specific group chat, and
    relinquish ownership to a studier if the scholar wishes.

###  

### 

## **3.2 External Interface Requirements**

See attached file \"not_lyft.jpeg\" for visual specifications.

![](vertopal_5fa18a1cfd294c50a15b46331ef6e02b/media/image1.png){width="6.5in"
height="5.791666666666667in"}

## **3.3 System Requirements**

1.  If a user chooses to video chat then they need to have atleast 64mb
    of video memory (Mac or PC)

2.  User must have access to a browser to connect to the SGs that they
    have joined and a connection of at least 500 Kbps

## **3.4 Nonfunctional Requirements**

1.  App layout should be simple, with a flow that easily connects users
    to groups that align with their study interests.

2.  Message receiving and sending should be responsive, allowing users
    to see if a message failed to deliver in case of lack of network
    connection.

3.  Users should only be able to see group messages in SG they have
    joined to prevent privacy leaks or mishandling.
    
    
    
| TASK                                      |    OWNER      |    Priority    |     Level of Effort (Estimate of days)     |   Additional Notes  |
| ---------------------------------------- | -------------  | -------------- | -------------------------------------      | ------------------- |
| Login and Signup (account functionality)  |  Sam | P1 | 7| Time-boxed task -- I'll do as much as I can in the 3 days | 
| Matchmaking quiz  | Robert  | P1  | 5  | Look up efficient ways for matching algorithms check out dating app types   |
| Matchmaking Profile Tags  | Sam  | P2  | 1  | Pull matchmaking quiz stats and compare each added user in gc 
