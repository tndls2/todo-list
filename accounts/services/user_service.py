from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import SlidingToken, AccessToken

from accounts.models import User
from core.base_service import BaseService
from core.exceptions import UserAlreadyExistsException, UserNotAuthenticatedException


class UserService(BaseService):
    model = User

    def __init__(self, user=None):
        super(UserService, self).__init__()
        self._user = user

    def login(self, user_name, password) -> dict:
        user = authenticate(user_name=user_name, password=password)
        # 사용자 정보 유효성 체크
        if user is None:
            raise UserNotAuthenticatedException()

        access_token = AccessToken.for_user(user)
        refresh_token = SlidingToken.for_user(user)
        jwt_token_output_dto = dict(
            access=str(access_token),
            refresh=str(refresh_token)
        )
        return jwt_token_output_dto

    def signup(self, user_name, password) -> dict:
        # user_name 중복 체크
        if self.check_available_user_name(user_name=user_name):
            raise UserAlreadyExistsException()

        user = User.objects.create_user(user_name=user_name, password=password)
        access_token = AccessToken.for_user(user)
        refresh_token = SlidingToken.for_user(user)
        jwt_token_output_dto = dict(
            access=str(access_token),
            refresh=str(refresh_token)
        )
        return jwt_token_output_dto

    def check_available_user_name(self, user_name) -> bool:
        is_exist = User.objects.filter(user_name=user_name).exists()
        return is_exist

    @property
    def user(self) -> User:
        return self._user
