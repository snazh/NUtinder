from src.models.user import GenderEnum
from better_profanity import profanity


class ValidationError(Exception):
    """Custom exception for validation errors."""

    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


class ValidationService:

    def __init__(self, data: dict):
        self.data = data

    def set_name(self) -> None:
        contains_profanity = profanity.contains_profanity(self.data["name"])

        if contains_profanity:
            raise ValidationError("Forbidden name")

    def set_description(self) -> None:

        if len(self.data["description"]) > 10000:
            raise ValidationError("Too long description")

    def set_nuid(self) -> None:

        if len(self.data["nu_id"]) > 9:
            raise ValidationError("Invalid NU id")

    def set_gender(self) -> None:
        gender = self.data["gender"].lower()

        if gender in ("female", "male"):
            self.data["gender"] = GenderEnum[gender]
        else:
            self.data["gender"] = GenderEnum["other"]

    def set_soulmate_gender(self) -> None:
        gender = self.data["soulmate_gender"].lower()
        if gender in ("female", "male"):
            self.data["soulmate_gender"] = GenderEnum[gender]
        else:
            self.data["soulmate_gender"] = GenderEnum["other"]

    def set_course(self) -> None:

        courses = ("NUFYP", "1st course", "2nd course",
                   "3rd course", "4th course", "Master degree",
                   "PhD degree", "Anonymous")

        if self.data["course"] not in courses:
            raise ValidationError("Not valid course")


def validate_data(data: dict) -> None:
    validation_service = ValidationService(data)

    for method_name in dir(validation_service):
        if method_name.startswith("set_"):
            method = getattr(validation_service, method_name)
            if callable(method):
                method()
