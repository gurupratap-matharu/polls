from django.urls import path
from users.views import UserDetailAPIView, UserListAPIView

urlpatterns = [
    path('<int:pk>/', UserDetailAPIView.as_view()),
    path('', UserListAPIView.as_view()),
]
