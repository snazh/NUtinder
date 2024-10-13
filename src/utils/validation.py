from src.models.enums import GenderEnum, SoulmateGenderEnum
from better_profanity import profanity


class ValidationError(Exception):
    """Custom exception for validation errors."""

    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


class Validation:
    @staticmethod
    async def set_name(name: str) -> None:
        contains_profanity = profanity.contains_profanity(name)

        if contains_profanity:
            raise ValidationError("Forbidden name")

        elif len(name) > 24:
            raise ValidationError("Too long name")

    @staticmethod
    async def set_desc(desc: str) -> None:
        if len(desc) > 2048:
            raise ValidationError("Too long description")

    @staticmethod
    async def set_gender(gender: str) -> GenderEnum:

        if gender not in ("female", "male"):
            raise ValidationError("Not valid gender")
        return GenderEnum[gender]

    @staticmethod
    async def set_soulmate_gender(gender) -> SoulmateGenderEnum:
        if gender not in ("female", "male", "all"):
            raise ValidationError("Not valid gender")
        return SoulmateGenderEnum[gender]

    @staticmethod
    async def set_photo(photo_url: str) -> None:
        if photo_url is None:
            raise ValidationError("Not valid photo")

    @staticmethod
    async def set_nuid(nu_id: str) -> None:
        if len(nu_id) != 9:
            raise ValidationError("Invalid NU id")

    @staticmethod
    async def set_course(course: str) -> None:
        courses = ("NUFYP", "1st course", "2nd course",
                   "3rd course", "4th course", "Master degree",
                   "PhD degree", "Anonymous")

        if course not in courses:
            raise ValidationError("Not valid course")
