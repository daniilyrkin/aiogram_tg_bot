from sqlalchemy import select, delete, insert
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import Birthday, User, Expenses, Investment, Product_list, LikeImage


dict_tables = {
    'Birthday': Birthday,
    'User': User,
    'Expenses': Expenses,
    'Investment': Investment,
    'Product_list': Product_list,
    'LikeImage': LikeImage}


async def orm_get(tablename: str, session: AsyncSession):
    query = select(dict_tables[tablename])
    result = await session.execute(query)
    return result.scalars().all()


async def orm_get_one(tablename: str, session: AsyncSession, kwargs=None):
    if kwargs is None:
        return await session.scalar(
            select(dict_tables[tablename]).order_by(dict_tables[tablename].id.desc()).limit(1))
    else:
        return await session.scalar(select(dict_tables[tablename]).filter_by(**kwargs if kwargs == dict else kwargs))


async def orm_add(tablename: str, session: AsyncSession, data: dict):
    item = await orm_get_one(tablename=tablename, session=session, kwargs=data)
    if not item:
        await session.execute(insert(dict_tables[tablename]).values(**data))
        await session.commit()


async def orm_update(session: AsyncSession, data: dict, tablename: str, kwargs):
    item = await session.scalar(select(dict_tables[tablename]).filter_by(**kwargs))
    if item:
        item = data
        await session.commit()


async def orm_delete(session: AsyncSession, tablename: str, **kwargs):
    item = await session.scalar(select(dict_tables[tablename]).filter_by(**kwargs))
    if item:
        await session.execute(delete(dict_tables[tablename]).filter_by(**kwargs))
        await session.commit()
