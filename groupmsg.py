class groupmsg:
    def __init__(self, group, sender, firstname, lastname, timestamp, message, profilepic):
        self.sender= sender
        self.lastname= lastname
        self.firstname= firstname
        self.group= group
        self.timestamp= str(timestamp)
        self.message= message
        self.profilepic= profilepic
       