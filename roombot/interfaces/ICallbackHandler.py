import aiogram


class ICallbackHandler:
    async def process_callback(self, callback: aiogram.types.CallbackQuery): ...

