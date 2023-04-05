class groupmsg: # pylint: disable=C0103, R0903
    """groupmsg class"""
    def __init__(self, group, sender, firstname, lastname, timestamp, message, profilepic): # pylint: disable=too-many-arguments
        """group message attributes"""
        self.sender= sender
        self.lastname= lastname
        self.firstname= firstname
        self.group= group
        self.timestamp= timestamp
        self.message= message
        self.profilepic= profilepic
       