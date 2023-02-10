class Group:
    def __init__(self, _id, name, users, createdTimestamp, desc, photo, messages):
        self._id= str(_id)
        self.name= name
        self.users= users
        self.createdTimestamp= createdTimestamp
        self.description = desc
        self.photo= photo
        self.messages= messages