import databases
import datetime
import aiogram
import json
import time

from messrooms.rooms import rc
from roombot.rooms_container.load_rooms_file import RoomsFile
from roombot import RoomsManager
from roombot import Sqlite3Users
from roombot import AiogramMiddleWare
from roombot import IMessageHandler
from roombot import IErrorHandler


class LogMess(IMessageHandler):
    def __init__(self): pass

    def process(self, message: aiogram.types.Message, **kwargs):
        print(f"{datetime.datetime.fromtimestamp(time.time()).strftime('%Y.%m.%d %H:%M')} | "
              f"{message.from_user.id}(@{message.from_user.username}, {message.from_user.first_name}): "
              f"{message.text}")


class LogError(IErrorHandler):
    def __init__(self): pass
    def process(self, exc: aiogram.types.Message, **kwargs): print(kwargs.get("text"))


database = databases.Database(
        f"sqlite:///data.db"
)

users = Sqlite3Users(database)


async def startup(*args, **kwargs): await database.connect()
async def shutdown(*args, **kwargs): await database.disconnect()


api_token = json.load(open("config.json", "r")).get("api_key")

bot = aiogram.Bot(api_token)
dispatcher = aiogram.Dispatcher(bot)

rb = RoomsManager(users, "start", include_default_handlers=True)
rb.append_rooms(RoomsFile("main.json", rb))
# rb.append_rooms(rc)
rb.add_message_handler(LogMess(), 0)
rb.add_error_handler(LogError())

rb.add_global_parameters(rb=rb, bot=bot, database=database)

dispatcher.middleware.setup(AiogramMiddleWare(rb))
aiogram.executor.start_polling(dispatcher, on_startup=startup, on_shutdown=shutdown)