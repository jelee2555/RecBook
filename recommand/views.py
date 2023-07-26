import datetime
import json

from django.http import JsonResponse
from rest_framework import status
from django.db import connection
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Recommand, Book, Like
from .serializers import RecommandSerializer, BookSerializer, LikeSerializer
from accounts.decorators import login_decorator


# Create your views here.
def set_age(age):
    if age <= 13:
        return '아동(0~13)'
    elif age <= 19:
        return '청소년(14~19)'
    elif age <= 29:
        return '20대'
    elif age <= 39:
        return '30대'
    elif age <= 49:
        return '40대'
    elif age <= 64:
        return '50~64세'
    else:
        return '65세이상'


class BookAPIView(APIView):

    # 전체 book 조회
    def get(self, request):
        book = Book.objects.all()
        serializer = BookSerializer(book, many=True)
        return Response(serializer.data)


class RecommandBookAPIView(APIView):
    # user의 연령, 성별에 따른 도서 추천
    @login_decorator
    def get(self, request):
        try:
            user = request.user
            # print('----------------- print user')
            # print(user.user_name)
            # print(user.user_password)

            gender = user.user_gender
            age_date = user.user_birth
            # print(datetime.datetime.now().year)
            # print(int(age_date.strftime("%Y")))
            age_num = datetime.datetime.now().year - int(age_date.strftime("%Y"))
            # print(age_num)
            age = set_age(age_num)

            # print('-----------------check gender')
            # print(gender)
            # print('-----------------check age')
            # print(age)

            cursor = connection.cursor()
            sql = "select recommand_class from recommandtbl where recommand_gender = %s and recommand_age = %s order by recommand_class_cnt desc limit 3;"
            data = (gender, age)
            cursor.execute(sql, data)
            class_result = cursor.fetchall()
            print('----------------------class result')
            print(class_result)
            class_data = []
            for i in class_result:
                class_data.append(i[0])
            print(class_data)
            x = class_data[0]

            total_result = ()
            for x in class_data:
                cursor2 = connection.cursor()
                sql2 = "select * from booktbl where book_class = %s order by book_id asc limit 5;"
                cursor2.execute(sql2, str(x))
                result = cursor2.fetchall()
                total_result += result

            # print('--------------- result')
            # print(total_result)

            book_list = []
            for data in total_result:
                book = Book()
                book.book_id = data[0]
                book.book_title = data[1]
                book.book_writer = data[2]
                book.book_publish = data[3]
                book.book_class = data[4]
                book_list.append(book)

            serializer = BookSerializer(book_list, many=True)
            return Response(serializer.data)

        except Exception as e:
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)


class LikeAPIView(APIView):
    #찜 목록에 책 저장하기
    @login_decorator
    def post(self, request):
        data = json.loads(request.body)
        book_id = data['book_id']
        like_object, created = Like.objects.get_or_create(book_id=book_id, user_id=request.user.user_id)
        if not created:
            like_object.delete()
            return Response(status=status.HTTP_200_OK)
        serializer = LikeSerializer(like_object)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    #찜 목록 책 데이터 불러오기
    @login_decorator
    def get(self, request):
        like_list = Like.objects.filter(user_id=request.user.user_id)
        book_list = []
        for like in like_list:
            print(like.book_id)
            book = Book.objects.get(book_id=like.book_id)
            book_list.append(book)
        serializer = BookSerializer(book_list, many=True)
        return Response(serializer.data)