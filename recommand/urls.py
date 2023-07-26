from django.urls import path
from . import views

urlpatterns = [
    path('', views.BookAPIView.as_view()),
    path('book/', views.RecommandBookAPIView.as_view()),
    path('like/', views.LikeAPIView.as_view()),
]