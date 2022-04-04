import aiogram
import traceback

from roombot.manager.manager import RoomsManager
from aiogram.dispatcher.middlewares import BaseMiddleware


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
        try:
            await self.rooms_manager.process_message(message)
        except Exception as e:
            await self.rooms_manager.process_error(e, traceback.format_exc())

    async def on_post_process_callback_query(self,
                                             callback: aiogram.types.CallbackQuery,
                                             results: tuple,
                                             data: dict
                                             ):
        try:
            await self.rooms_manager.process_callback(callback)
        except Exception as e:
            await self.rooms_manager.process_error(e, traceback.format_exc())

    async def on_post_process_pre_checkout_query(self,
                                                 pre_checkout_query: aiogram.types.PreCheckoutQuery,
                                                 results: tuple,
                                                 data: dict
                                                 ):
        try:
            await self.rooms_manager.process_pre_checkout_query(pre_checkout_query)
        except Exception as e:
            await self.rooms_manager.process_error(e, traceback.format_exc())

