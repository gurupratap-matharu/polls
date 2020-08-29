from django.urls import path

from classroom.views import ClassroomDetailView, ClassroomListView

urlpatterns = [
    path('', ClassroomListView.as_view(), name='classroom_list'),
    path('<uuid:pk>/', ClassroomDetailView.as_view(), name='classroom_detail'),
]
