import aiogram

from roombot.manager.manager import RoomsManager
from roombot.interfaces.IBot import IBot
from aiogram.dispatcher.middlewares import BaseMiddleware


class MessageTypes:
    TEXT = "text"
    AUDIO = "audio"
    DOCUMENT = "document"
    GAME = "game"
    PHOTO = "photo"
    STICKER = "sticker"
    VIDEO = "video"
    VIDEO_NOTE = "video_note"
    VOICE = "voice"
    CONTACT = "contact"
    LOCATION = "location"
    VENUE = "venue"
    NEW_CHAT_MEMBERS = "new_chat_members"
    LEFT_CHAT_MEMBER = "left_chat_member"
    INVOICE = "invoice"
    SUCCESSFUL_PAYMENT = "successful_payment"
    CONNECTED_WEBSITE = "connected_website"
    MIGRATE_TO_CHAT_ID = "migrate_to_chat_id"
    MIGRATE_FROM_CHAT_ID = "migrate_from_chat_id"
    UNKNOWN = "unknown"
    ANY = "any"


class AiogramMiddleWare(BaseMiddleware):
    bot: aiogram.Bot
    dispatcher: aiogram.Dispatcher

    def __init__(self, rooms_manager: RoomsManager):
        self.rooms_manager = rooms_manager
        super().__init__()

    async def on_post_process_message(self,
                                      message: aiogram.types.Message,
                                      results: tuple,
                                      data: dict
                                      ):
        await self.rooms_manager.process_message(message)

    async def on_post_process_callback_query(self,
                                             callback: aiogram.types.CallbackQuery,
                                             results: tuple,
                                             data: dict
                                             ):
        await self.rooms_manager.process_callback(callback)

