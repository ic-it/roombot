import aiogram


class IMessageHandler:
    async def process_message(self, message: aiogram.types.Message): ...

