import asyncio

from aiohttp import web

from chat import views
from config import DATABASE
from database import async_db_session, AsyncDatabaseSession

app = web.Application()


def create_app():
    """Инициализация приложения"""
    loop = asyncio.get_event_loop()
    loop.run_until_complete(setup())


async def setup():
    await async_db_session.init()
    await async_db_session.create_all()


if __name__ == '__main__':
    create_app()

    app.add_routes([web.get('/', setup)])
    app.add_routes([web.get('/add_user/', views.add_user)])
    app.add_routes([web.get('/get_user/', views.get_user)])
    web.run_app(app)
