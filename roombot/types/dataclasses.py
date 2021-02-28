from dataclasses import dataclass


@dataclass
class User:
    telegram_id: int
    firstname: str
    lastname: str
    permissions: str
    room: str
    id: int = None

    def as_list(self):
        if self.id:
            return [self.telegram_id, self.firstname, self.lastname, self.permissions, self.room, self.id]
        else:
            return [self.telegram_id, self.firstname, self.lastname, self.permissions, self.room]

    def as_dict(self):
        return {"telegram_id": self.telegram_id,
                "firstname": self.firstname,
                "lastname": self.lastname,
                "permissions": self.permissions,
                "room": self.room,
                "id": self.id
                }
