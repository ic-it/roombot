import aiogram


class IMessageHandler:
    async def process(self, message: aiogram.types.Message, **kwargs): ...
