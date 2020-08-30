from django.urls import path

from classroom.views import (ClassroomCreate, ClassroomDelete,
                             ClassroomDetailView, ClassroomListView,
                             ClassroomUpdate)

urlpatterns = [
    path('', ClassroomListView.as_view(), name='classroom_list'),
    path('<uuid:pk>/', ClassroomDetailView.as_view(), name='classroom_detail'),
    path('create/', ClassroomCreate.as_view(), name='classroom_create'),
    path('<uuid:pk>/update/', ClassroomUpdate.as_view(), name='classroom_update'),
    path('<uuid:pk>/delete/', ClassroomDelete.as_view(), name='classroom_delete'),
]
