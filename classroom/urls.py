from django.urls import path

from classroom.views import ClassroomListView

urlpatterns = [
    path('', ClassroomListView.as_view(), name='classroom_list'),
]
