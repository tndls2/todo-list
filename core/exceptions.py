from rest_framework.exceptions import APIException


class UserAlreadyExistsException(APIException):
    status_code = 400
    default_detail = '사용자 정보가 중복으로 존재합니다.'


class UserNotAuthenticatedException(APIException):
    status_code = 401
    default_detail = "사용자 정보가 일치하지 않습니다."
