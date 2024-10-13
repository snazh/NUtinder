# src/models/enums.py

import enum


class GenderEnum(enum.Enum):
    male = "male"
    female = "female"


class SoulmateGenderEnum(enum.Enum):
    male = "male"
    female = "female"
    all = "all"


class EvalEnum(enum.Enum):
    like: str = "like"
    dislike: str = "dislike"
