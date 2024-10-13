from src.models.user import User
from src.utils.sqlalchemy_repo import SQLAlchemyRepository


class UserRepository(SQLAlchemyRepository):
    model = User
