from aiohttp import web
from loguru import logger

from helpers.exceptions import HandledException


def catch_exception(func):
    """
    Декоратор, отлавливающий все исключения.
    Логирует исключение и возвращает HTTP Response 400.
     """
    async def helper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except HandledException as e:
            return web.Response(status=400, text=e.text)
        except Exception as e:
            logger.error(e)
            return web.Response(status=400, text='Неизвестная ошибка')
    return helper

