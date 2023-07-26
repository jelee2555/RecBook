import jwt
from django.http import JsonResponse

from RecBook import settings
from RecBook.settings import SECRET_KEY
from accounts.models import User


def login_decorator(func):
    def wrapper(self, request, *args, **kwargs):
        try:
            access = request.COOKIES.get('access_token')
            payload = jwt.decode(access, SECRET_KEY, algorithms=['HS256'])
            user = User.objects.get(user_id=payload["user_id"])
            request.user = user
        except jwt.exceptions.DecodeError:
            return JsonResponse({"message": "INVALID_TOKEN"}, status=400)
        except User.DoesNotExist:
            return JsonResponse({"message": "INVALID_USER"}, status=400)
        return func(self, request, *args, **kwargs)
    return wrapper