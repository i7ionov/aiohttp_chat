import config
import os
# перед импортом остальных модулей поменяем путь к базе
db_path = os.path.join(config.BASE_DIR, 'test_sqlite3.db')
config.DATABASE = 'sqlite+aiosqlite:///' + db_path

from unittest import IsolatedAsyncioTestCase
from app import setup
from chat.models import User

from chat.services import UserService, ChatService, MessageService, UserAlreadyExistsException
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
        created_user = await User.get(user.id)
        try:
            user = await UserService.create(login='user', password='password')
        except UserAlreadyExistsException:
            pass
        else:
            raise AssertionError
