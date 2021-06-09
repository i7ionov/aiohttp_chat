from typing import Union

import sqlalchemy
from sqlalchemy.exc import IntegrityError

from chat.models import User, Chat, Message
from database import async_db_session
from helpers.exceptions import HandledException


class UserAlreadyExistsException(HandledException):
    text = 'Пользователь с таким логином уже зарегистрирован'

class UserService:
    @classmethod
    async def create(cls, **kwargs):
        users = await User.filter(User.login==kwargs['login'])
        if users:
            raise UserAlreadyExistsException
        user = await User.create(**kwargs)
        return user

    @classmethod
    async def update(cls, item_id, **kwargs):
        pass


class ChatService:
    pass


class MessageService:
    pass
