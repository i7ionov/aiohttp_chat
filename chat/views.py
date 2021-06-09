import sqlalchemy
from aiohttp import web

from chat.models import User
from chat.services import UserService
from helpers.decorators import catch_exception


@catch_exception
async def add_user(request):
    """Дбавление нового пользователя"""
    if 'login' in request.query and 'password' in request.query:
        await UserService.create(**request.query)
        return web.Response(status=201, text='Пользователь зарегистрирован')
    else:
        return web.Response(status=400, text='Не указан логин и пароль')

#@catch_exception
async def get_user(request):
    """Дбавление нового пользователя"""
    if 'id' in request.query:
        user = await User.get(request.query['id'])
        return web.Response(status=201, text=user.login)
    else:
        return web.Response(status=400, text='Не указан id')
