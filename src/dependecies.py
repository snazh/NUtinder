from src.repositories.profile_repo import ProfileRepository, ProfileEvalRepository
from src.repositories.user_repo import UserRepository
from src.services.profile_service import ProfileService, ProfileEvalService
from src.services.user_management import UserService


def get_profile_service():
    return ProfileService(profile_repo=ProfileRepository)


def get_user_service():
    return UserService(user_repo=UserRepository)


def get_profile_eval_service():
    return ProfileEvalService(profile_eval_repo=ProfileEvalRepository)


