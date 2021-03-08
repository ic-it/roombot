from .IHandler import IHandler


class IErrorHandler(IHandler):
    async def process(self, exception: Exception): ...