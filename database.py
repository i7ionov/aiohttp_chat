from sqlalchemy import Column, Integer, select
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from sqlalchemy import update as sqlalchemy_update
from config import DATABASE

Base = declarative_base()
async_db_session = None

class AsyncDatabaseSession:
    def __init__(self):
        self._session = None
        self._engine = None

    def __getattr__(self, name):
        return getattr(self._session, name)

    async def init(self, ):
        self._engine = create_async_engine(DATABASE,
            echo=False,
        )

        self._session = sessionmaker(
            self._engine, expire_on_commit=False, class_=AsyncSession
        )()

    async def create_all(self):
        async with self._engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)


class ModelAdmin:
    @classmethod
    async def create(cls, **kwargs):
        item = cls(**kwargs)
        async_db_session.add(item)
        await async_db_session.commit()
        return item

    @classmethod
    async def update(cls, id, **kwargs):
        query = (
            sqlalchemy_update(cls)
                .where(cls.id == id)
                .values(**kwargs)
                .execution_options(synchronize_session="fetch")
        )
        await async_db_session.execute(query)
        await async_db_session.commit()

    @ classmethod
    async def get(cls, id):
        query = select(cls).where(cls.id == id)
        results = await async_db_session.execute(query)
        (result,) = results.one()
        return result

    @classmethod
    async def filter(cls,*args, **kwargs):
        query = select(cls).where(*args,**kwargs)
        results = await async_db_session.execute(query)
        result = []
        for res in results:
            result.append(res)
        return result

class BaseModel(Base, ModelAdmin):
    __abstract__ = True
    id = Column(Integer, unique=True, primary_key=True, autoincrement=True)

    def __repr__(self):
        return "<{0.__class__.__name__}(id={0.id!r})>".format(self)

async_db_session = AsyncDatabaseSession()
