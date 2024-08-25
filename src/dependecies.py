

from src.services.user_management import UserProfileService, UserService
from src.user_repository import UserProfileRepository, UserRepository


def get_user_profile_service():
    return UserProfileService(users_repo=UserProfileRepository)


def get_user_service():
    return UserService(users_repo=UserRepository)




