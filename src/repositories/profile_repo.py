from src.models.profile import ProfileEval, Profile, ProfileHistory
from src.utils.sqlalchemy_repo import SQLAlchemyRepository


class ProfileRepository(SQLAlchemyRepository):
    model = Profile


class ProfileHistoryRepository(SQLAlchemyRepository):
    model = ProfileHistory


class ProfileEvalRepository(SQLAlchemyRepository):
    model = ProfileEval
