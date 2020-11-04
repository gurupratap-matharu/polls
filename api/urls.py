from django.urls import path
from polls.views import QuestionDetailAPIView, QuestionListAPIView
from users.views import (ProfileDetailAPIView, ProfileListAPIView,
                         UserDetailAPIView, UserListAPIView)

urlpatterns = [
    path('users/<int:pk>/', UserDetailAPIView.as_view()),
    path('users/', UserListAPIView.as_view()),
    path('profile/', ProfileListAPIView.as_view()),
    path('profile/<uuid:pk>/', ProfileDetailAPIView.as_view()),
    path('polls/', QuestionListAPIView.as_view()),
    path('polls/<uuid:pk>/', QuestionDetailAPIView.as_view()),
]
