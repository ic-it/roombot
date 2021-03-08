import aiogram


class ICallbackHandler:
    async def process(self, callback: aiogram.types.CallbackQuery): ...

