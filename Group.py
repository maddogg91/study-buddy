class Group: # pylint: disable=C0103, R0903, C0114
    """creates basic group"""
    def __init__(self, _id, name, users, created_timestamp, desc, photo, messages):
        """class group attributes"""
        self._id= str(_id)
        self.name= name
        self.users= users
        self.created_timestamp= str(created_timestamp)
        self.description = desc
        self.photo= photo
        self.messages= messages
