import config
import os
# перед импортом остальных модулей поменяем путь к базе
db_path = os.path.join(config.BASE_DIR, 'test_sqlite3.db')
config.DATABASE = 'sqlite+aiosqlite:///' + db_path

from unittest import IsolatedAsyncioTestCase
from app import setup
from chat.models import User, Chat

from chat.services import UserService, ChatService, MessageService, UserAlreadyExistsException, \
    UserDoesNotExistsException
from database import async_db_session


class BaseTest(IsolatedAsyncioTestCase):

    async def asyncSetUp(self) -> None:
        """Инициализация тестовой базы"""
        await setup()

    async def asyncTearDown(self) -> None:
        """Удаление тестовой базы"""
        await async_db_session.close()
        if os.path.isfile(db_path):
            os.remove(db_path)


class UserServiceTest(BaseTest):
    async def test_creating_user(self):
        user = await UserService.create(login='user', password='password')
        created_user = await User.get(user.id)
        self.assertEqual(user, created_user)

    async def test_raise_error_if_user_already_exists(self):
        user = await UserService.create(login='user', password='password')
        try:
            user = await UserService.create(login='user', password='password')
        except UserAlreadyExistsException:
            pass
        else:
            raise AssertionError

    async def test_updating_user(self):
        user = await UserService.create(login='user', password='password')
        user = await UserService.update(user.id ,login='new_user', password='new_password')
        updated_user = await User.get(user.id)
        self.assertEqual(updated_user.login, 'new_user')
        self.assertEqual(updated_user.password, 'new_password')

    async def test_updating_not_existing_user_raise_error(self):
        not_existing_id = 999
        try:
            user = await UserService.update(not_existing_id ,login='new_user', password='new_password')
        except UserDoesNotExistsException:
            pass
        else:
            raise AssertionError


class ChatServiceTest(BaseTest):
    async def test_creating_chat(self):
        user1 = await UserService.create(login='User1', password='123')
        user2 = await UserService.create(login='User2', password='123')
        user3 = await UserService.create(login='User3', password='123')
        chat = await ChatService.create(name='Test chat', owner=user1, users=[user2])
        created_chat = await Chat.get(chat.id)
        self.assertEqual(chat.name, created_chat.name)
        self.assertEqual(chat.owner, created_chat.owner)
        # в списке членов чата должн быть и владелец чата
        self.assertSetEqual(set(chat.users), {user1, user2})

    async def test_creating_chat_with_not_existing_user_raise_error(self):
        not_existing_id = 999
        user3 = await UserService.create(login='User3', password='123')
        try:
            chat = await ChatService.create(name='Test chat', owner_id=not_existing_id)
        except UserDoesNotExistsException:
            pass
        else:
            raise AssertionError

