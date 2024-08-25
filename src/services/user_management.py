import asyncio
from typing import List

from src.models.user import UserProfile, User
from src.utils.sqlalchemy_repo import SQLAlchemyRepository


class UserProfileService:
    def __init__(self, profiles_repo):
        self.profiles_repo: SQLAlchemyRepository = profiles_repo()

    async def create_profile(self, user_data: dict) -> int:
        user_id = await self.profiles_repo.add_one(user_data)
        return user_id

    async def get_all_profiles(self) -> List[dict]:
        users = await self.profiles_repo.get_all()
        return users

    async def get_latest_profile(self, tg_id: int) -> dict | None:

        profiles = await self.profiles_repo.join_tables_by_param(tb2=User, tb2_fk="user_id", attribute="tg_id",
                                                                 value=tg_id)

        if not profiles:
            return None
        latest_profile = profiles[0]
        for profile in profiles:
            if profile["registered_at"] > latest_profile["registered_at"]:
                latest_profile = profile

        return latest_profile

    # async def get_male_anketas(self):
    #     profiles = await self.profiles_repo.join_tables_by_param(tb2=User, tb2_fk="user_id", attribute="tg_id",
    #                                                           value=tg_id)

    async def get_female_anketas(self):
        profiles = await self.profiles_repo.join_tables_by_param()


class UserService:
    def __init__(self, users_repo):
        self.users_repo: SQLAlchemyRepository = users_repo()

    async def add_user(self, user_data: dict) -> int:
        user_id = await self.users_repo.add_one(user_data)
        return user_id

    async def get_specific_user(self, tg_id: int) -> dict:
        user = await self.users_repo.filter(filter_column="tg_id", value=tg_id)
        return user[0]
