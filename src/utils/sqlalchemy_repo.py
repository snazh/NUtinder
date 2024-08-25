from abc import ABC, abstractmethod
import asyncio
from typing import List, Any

from sqlalchemy import insert, select, delete, text

from src.database.connector import async_session_maker
from src.models.user import UserProfile, GenderEnum, User


class AbstractRepository(ABC):  # Abstract layer for CRUD initialization
    @abstractmethod
    async def add_one(self, data: dict):
        raise NotImplementedError

    @abstractmethod
    async def get_all(self):
        raise NotImplementedError

    @abstractmethod
    async def get_one(self, entity_id: int):
        raise NotImplementedError

    @abstractmethod
    async def delete_one(self, entity_id: int):
        raise NotImplementedError

    @abstractmethod
    async def filter(self, filter_column: str, value: int | str):
        return NotImplementedError

    @abstractmethod
    async def join_tables_by_param(self, tb2, tb2_fk: str, attribute: str, value: Any):
        raise NotImplementedError


# repository for basic CRUD operations
class SQLAlchemyRepository(AbstractRepository):
    model = None

    def _to_dict(self, entity):
        """Convert SQLAlchemy model instance to dictionary"""
        return {column.name: getattr(entity, column.name) for column in entity.__table__.columns}

    async def add_one(self, data: dict) -> int:  # returns record's pk
        async with async_session_maker() as session:
            stmt = insert(self.model).values(**data).returning(self.model.id)
            result = await session.execute(stmt)
            await session.commit()
            return result.scalar_one()

    async def get_all(self) -> list[dict]:  # returns all records
        async with async_session_maker() as session:
            stmt = select(self.model)
            result = await session.execute(stmt)
            result = [row[0] for row in result.all()]
            return result

    async def get_one(self, entity_id: int) -> dict | None:  # returns specific record
        async with async_session_maker() as session:
            query = select(self.model).where(self.model.id == entity_id)
            result = await session.execute(query)
            entity = result.scalar_one_or_none()
            return entity

    async def delete_one(self, entity_id: int) -> None:  # delete specific record
        async with async_session_maker() as session:
            stmt = delete(self.model).where(self.model.id == entity_id)
            await session.execute(stmt)
            await session.commit()

    async def filter(self, filter_column: str, value: int | str) -> List[dict]:
        async with async_session_maker() as session:
            query = select(self.model).filter(getattr(self.model, filter_column) == value)
            result = await session.execute(query)
            entities = result.scalars().all()
            return [self._to_dict(entity) for entity in entities]

    async def join_tables_by_param(self, tb2, tb2_fk: str, attribute: str, value: Any) -> List[dict]:
        async with async_session_maker() as session:
            stmt = (
                select(tb2, self.model)
                .outerjoin(tb2, getattr(tb2, "id") == getattr(self.model, tb2_fk))
                .where(getattr(tb2, attribute) == value)
            )

            result = await session.execute(stmt)
            entities = result.fetchall()

            # Convert the result to a list of dictionaries
            joined_results = []
            for entity1, entity2 in entities:
                entity1_dict = {col.name: getattr(entity1, col.name) for col in entity1.__table__.columns}
                entity2_dict = {col.name: getattr(entity2, col.name) for col in entity2.__table__.columns}
                # Combine both dictionaries into one
                combined_dict = {**entity1_dict, **entity2_dict}
                joined_results.append(combined_dict)

            return joined_results

    async def raw_custom_query(self, sql_query: str):
        async with async_session_maker() as session:

            query = text(sql_query)

            # Execute the query
            result = await session.execute(query)

            # Fetch all results as dictionaries
            rows = result.mappings().all()

        return [dict(row) for row in rows]

    async def update_one(self, entity_id):  # todo
        pass

async def main():
    instance = SQLAlchemyRepository()
    instance.model = UserProfile

    results = await instance.raw_custom_query(sql_query="SELECT DISTINCT ON (user_id) * "
                                                        "FROM profile "
                                                        "ORDER BY user_id, registered_at DESC")
    print(results)


asyncio.run(main())
