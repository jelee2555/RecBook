import jwt
from django.contrib.auth import authenticate
from django.db import connection
from django.shortcuts import render, get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from RecBook.settings import SECRET_KEY
from accounts.models import User
from accounts.serializers import UserSerializer


# Create your views here.
class RegisterAPIView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            # access jwt token
            token = TokenObtainPairSerializer.get_token(user)
            refresh_token = str(token)
            access_token = str(token.access_token)
            res = Response(
                {
                    "user": serializer.data,
                    "message": "register success",
                    "token": {
                        "access": access_token,
                        "refresh": refresh_token,
                    },
                },
                status=status.HTTP_200_OK
            )

            res.set_cookie("access", access_token, httponly=True)
            res.set_cookie("refresh", refresh_token, httponly=True)

            return res
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AuthAPIView(APIView):
    def get(self, request):
        try:
            # print('------------token available')

            # access = request.COOKIES['access']
            access = request.COOKIES.get('access')
            print(access)
            payload = jwt.decode(access, SECRET_KEY, algorithms=['HS256'])
            # print('-----------------------jwt??')
            pk = payload.get('user_id')
            user = get_object_or_404(User, pk=pk)
            print('------------------------ print user')
            print(user)
            print('------------ pk')
            print(pk)
            serializer = UserSerializer(instance=user)
            return Response(serializer.data, status=status.HTTP_200_OK)

        # token 만료 시 새 토큰 발급
        except(jwt.exceptions.ExpiredSignatureError):
            data = {'refresh': request.COOKIES.get('refresh', None)}
            serializer = TokenObtainPairSerializer(data=data)
            if serializer.is_valid(raise_exception=True):
                access = serializer.data.get('access_token', None)
                refresh = serializer.data.get('refresh_token', None)
                payload = jwt.decode(access, SECRET_KEY, algorithms=['HS256'])
                pk = payload.get('user_id')
                user = get_object_or_404(User, pk=pk)
                serializer = UserSerializer(instance=user)
                res = Response(serializer.data, status=status.HTTP_200_OK)
                res.set_cookie('access_token', access)
                res.set_cookie('refresh_token', refresh)
                return res
            raise jwt.exceptions.InvalidTokenError

        # 사용 불가능한 토큰일 경우
        except(jwt.exceptions.InvalidTokenError):
            return Response(status=status.HTTP_400_BAD_REQUEST)

    #로그인
    def post(self, request):
        user_data = request.data
        user_data['user_password'] = user_data.pop('password')
        # print(user_data)
        user = User.objects.get(user_name=user_data['user_name'], user_password=user_data['user_password'])
        print(user)

        if user is not None:
            serializer = UserSerializer(user)
            token = TokenObtainPairSerializer.get_token(user)

            refresh_token = str(token)
            access_token = str(token.access_token)

            res = Response(
                {
                    "user": serializer.data,
                    "message": "login success",
                    "token": {
                        "access": access_token,
                        "refresh": refresh_token,
                    },
                },
                status=status.HTTP_200_OK,
            )
            res.set_cookie("access_token", access_token, httponly=True)
            res.set_cookie("refresh_token", refresh_token, httponly=True)

            return res
        return Response(status=status.HTTP_400_BAD_REQUEST)

    # 로그아웃
    def delete(self, request):
        response = Response({
            "message": "Logout success"
        }, status=status.HTTP_202_ACCEPTED)
        response.delete_cookie("access_token")
        response.delete_cookie("refresh_token")
        return response
