
from src.utils.sqlalchemy_repo import SQLAlchemyRepository


class UserService:
    def __init__(self, user_repo):
        self.user_repo: SQLAlchemyRepository = user_repo()

    async def add_user(self, user_data: dict) -> None:
        await self.user_repo.add_one(user_data)

    async def get_user(self, user_id: int) -> dict:
        user = await self.user_repo.get_one(user_id)
        return user

    async def get_user_by_tg_id(self, tg_id: int) -> dict:
        user = await self.user_repo.filter(filter_column="tg_id", value=tg_id)
        return user[0]
