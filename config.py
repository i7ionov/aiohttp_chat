import os

from loguru import logger

BASE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)))

DATABASE = 'sqlite+aiosqlite:///' + os.path.join(BASE_DIR, 'sqlite3.db')

logger.add(os.path.join(BASE_DIR, 'requests.log'), rotation="1 month", enqueue=True)