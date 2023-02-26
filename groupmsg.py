class groupmsg:
    def __init__(self, group, sender, timestamp, message):
        self.sender= sender
        self.group= group
        self.timestamp= str(timestamp)
        self.message= message
       