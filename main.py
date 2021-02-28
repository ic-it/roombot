import aiogram

from messrooms.rooms import rc

from roombot import RoomsManager
from roombot import Sqlite3Database
from roombot import JsonDatabase
from roombot import AiogramMiddleWare
from roombot import IMessageHandler


class LogMess(IMessageHandler):
    def __init__(self):
        pass

    def process_message(self, message: aiogram.types.Message):
        print(f"{message.from_user.id}({message.from_user.username}): {message.text}")


db = Sqlite3Database("data.db")
db.connect()
users = db.users

# db = JsonDatabase("data.json")
# db.connect()
# users = db.users


api_token = "1348518529:AAFg_7fSGQdNd78xQo3xWxtRWMJHCTG2OVw"

bot = aiogram.Bot(api_token)
dispatcher = aiogram.Dispatcher(bot)


rb = RoomsManager(users, "start", include_default_handlers=True)
rb.append_rooms(rc)
rb.add_message_handler(LogMess())
dispatcher.middleware.setup(AiogramMiddleWare(rb))
rb.add_global_parameters(rb=rb, bot=bot)
aiogram.executor.start_polling(dispatcher)
