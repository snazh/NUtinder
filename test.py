import asyncio

from sqlalchemy import insert

from src.models.user import User
from src.models.profile import Profile
from src.models.enums import SoulmateGenderEnum, GenderEnum
from src.database.connector import async_session_maker
import random as rd

photo_url = "AgACAgIAAxkBAAIE-WbQBlnsyVLhjvJKgGbJlTJZhqv8AALg4DEbKROASgVXZJ0eaZkQAQADAgADeAADNQQ"


# tg_id = "5259486580" + "10"

#
async def create_users():
    async with async_session_maker() as session:
        for i in range(20):
            tg_id = rd.randint(1000000000, 9999999999)

            print(tg_id)
            stmt = insert(User).values(tg_id=tg_id)

            await session.execute(stmt)
            await session.commit()


async def create_profiles():
    async with async_session_maker() as session:
        courses = ("NUFYP", "1st course", "2nd course",
                   "3rd course", "4th course", "Master degree",
                   "PhD degree", "Anonymous")

        genders = ("male", "female")
        soulmate_genders = ("male", "female", "all")
        for i in range(11, 31):
            data = {
                "user_id": i,
                "nu_id": str(rd.randint(100000000, 999999999)),
                "name": f"user{i}",
                "course": courses[rd.randint(0, 7)],
                "gender": GenderEnum[genders[rd.randint(0, 1)]],
                "soulmate_gender": SoulmateGenderEnum[soulmate_genders[rd.randint(0, 2)]],
                "description": "some text bla bla bla",
                "photo_url": photo_url
            }
            stmt = insert(Profile).values(**data)
            await session.execute(stmt)
            await session.commit()





asyncio.run(create_profiles())