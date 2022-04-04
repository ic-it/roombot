class User:
    telegram_id: int
    firstname: str
    lastname: str
    permissions: str
    room: str
    id: int
    additional_data: dict

    def __init__(self,
                 telegram_id: int,
                 firstname: str,
                 lastname: str,
                 permissions: str,
                 room: str,
                 id: int = None,
                 **additional_data):
        self.id = id
        self.room = room
        self.lastname = lastname
        self.permissions = permissions
        self.firstname = firstname
        self.telegram_id = telegram_id
        self.additional_data = additional_data

    def as_list(self):
        if self.id:
            return [self.telegram_id, self.firstname, self.lastname, self.permissions, self.room, self.id]
        else:
            return [self.telegram_id, self.firstname, self.lastname, self.permissions, self.room]

    def as_dict(self):
        data = {"telegram_id": self.telegram_id,
                "firstname": self.firstname,
                "lastname": self.lastname,
                "permissions": self.permissions,
                "room": self.room,
                "id": self.id
                }
        if not self.id:
            data.pop("id")
        data.update(self.additional_data)
        return data
