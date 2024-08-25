from src.models.user import UserProfile, User
from src.utils.sqlalchemy_repo import SQLAlchemyRepository


class UserProfileRepository(SQLAlchemyRepository):
    model = UserProfile


class UserRepository(SQLAlchemyRepository):
    model = User
