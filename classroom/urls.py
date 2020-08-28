from django.urls import path

from classroom.views import ClassroomListView

app_name = 'classroom'
urlpatterns = [
    path('', ClassroomListView.as_view(), name='classroom_list'),
]
