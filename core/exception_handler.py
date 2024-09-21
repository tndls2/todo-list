from rest_framework.response import Response
from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        # 예외가 처리된 경우, 'data' 필드에 예외 정보 담기
        custom_response = {
            'status_code': response.status_code,
            'message': response.status_text,
            'data': {
                'detail': response.data.get('detail', str(exc))
            }
        }
        return Response(custom_response, status=response.status_code)

    return response
