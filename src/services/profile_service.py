import asyncio
from typing import List, Any

from src.models.user import User
from src.utils.sqlalchemy_repo import SQLAlchemyRepository


class ProfileService:
    def __init__(self, profile_repo):
        self.profile_repo: SQLAlchemyRepository = profile_repo()

    async def create_profile(self, user_data: dict) -> None:
        await self.profile_repo.add_one(user_data)

    async def get_all_profiles(self) -> List[dict]:
        users = await self.profile_repo.get_all()
        return users

    async def update_profile(self, profile_id, column: str, value: Any) -> None:
        await self.profile_repo.update_one(entity_id=profile_id,
                                           column=column,
                                           value=value)

    async def get_profile_by_tg_id(self, tg_id: int) -> dict | None:
        profile = await self.profile_repo.join_tables_by_param(tb2=User, tb2_fk="user_id", attribute="tg_id",
                                                               value=tg_id)
        if not profile:
            return None
        return profile[0]

    async def get_profiles_by_gender(self, gender: str) -> List[dict]:
        profiles = await self.profile_repo.raw_custom_query(sql_query="SELECT DISTINCT ON (user_id) * "
                                                                      "FROM profile "
                                                                      "ORDER BY user_id, registered_at DESC")

        if gender == "all":
            return profiles

        specific_profiles = [pr for pr in profiles if pr["gender"] == gender]

        return specific_profiles


class ProfileEvalService:
    def __init__(self, profile_eval_repo):
        self.profile_repo: SQLAlchemyRepository = profile_eval_repo()

    async def evaluate(self, eval_data: dict) -> None:
        await self.profile_repo.add_one(eval_data)

    async def get_evaluated_profiles_ids(self, valuer_id: int) -> List[int]:
        profiles = await self.profile_repo.filter(filter_column="lover_id", value=f"{valuer_id}")
        profiles_ids = [profile["id"] for profile in profiles]
        return profiles_ids
