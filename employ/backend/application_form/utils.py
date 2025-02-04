import jwt
from django.conf import settings
from rest_framework.exceptions import AuthenticationFailed
from account.models import User

def get_company_from_token(request):
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        raise AuthenticationFailed('토큰이 필요합니다.')

    token = auth_header.split(' ')[1]

    try:
        decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed('토큰이 만료되었습니다.')
    except jwt.InvalidTokenError:
        raise AuthenticationFailed('유효하지 않은 토큰입니다.')

    user_id = decoded_token.get('user_id')
    if not user_id:
        raise AuthenticationFailed('유효한 사용자 정보가 없습니다.')

    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        raise AuthenticationFailed('사용자를 찾을 수 없습니다.')

    return user.company