from typing import Union

import sqlalchemy
from sqlalchemy.exc import IntegrityError, NoResultFound

from chat.models import User, Chat, Message
from database import async_db_session
from helpers.exceptions import HandledException


class UserAlreadyExistsException(HandledException):
    text = 'Пользователь с таким логином уже зарегистрирован'

class UserDoesNotExistsException(HandledException):
    text = 'Пользователь с такими данными не найден'

class UserService:
    @classmethod
    async def create(cls, **kwargs):
        found_users = await User.filter(User.login==kwargs['login'])
        if found_users:
            raise UserAlreadyExistsException
        user = await User.create(**kwargs)
        return user

    @classmethod
    async def update(cls, item_id, **kwargs):
        try:
            await User.update(item_id,**kwargs)
            return await User.get(item_id)
        except NoResultFound:
            raise UserDoesNotExistsException


class ChatAlreadyExistsException(HandledException):
    text = 'Чат с таким названием уже существует'


class ChatService:
    @classmethod
    async def create(cls, owner_id, **kwargs):
        found_chats = await Chat.filter(Chat.name==kwargs['name'])
        if found_chats:
            raise ChatAlreadyExistsException
        try:
            await User.get(owner_id)
        except NoResultFound:
            raise UserDoesNotExistsException
        if 'users' in kwargs:
            kwargs['users'].append(kwargs['owner'])
        chat = await Chat.create(owner_id=owner_id, **kwargs)
        return chat

    @classmethod
    async def update(cls, item_id, owner_id, **kwargs):
        try:
            user = await User.get(owner_id)
        except NoResultFound:
            raise UserDoesNotExistsException
        try:
            await Chat.update(item_id,**kwargs)
            return await Chat.get(item_id)
        except NoResultFound:
            raise UserDoesNotExistsException


class MessageService:
    pass
