from sqlalchemy import text
from sqlalchemy.exc import ProgrammingError, DBAPIError

from db.sqlalcem import async_session

async def create_partioning_tables(number: int, table_name: str) -> None:

    async with async_session() as session:

        for i in range(number):
            stmt = f'''CREATE TABLE {table_name}_{i+1} PARTITION OF {table_name}
                        FOR VALUES WITH (MODULUS {number}, REMAINDER {i})'''
            try:
                await session.execute(text(stmt))
            except (ProgrammingError, DBAPIError):
                continue
        await session.commit()