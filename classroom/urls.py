from django.urls import path

from classroom.views import (ClassroomCreate, ClassroomDelete,
                             ClassroomDetailView, ClassroomListView,
                             ClassroomPeopleView, ClassroomUpdate,
                             EnrollmentCreate, EnrollmentDelete)

urlpatterns = [
    path('', ClassroomListView.as_view(), name='classroom_list'),
    path('tag/<slug:tag_slug>/', ClassroomListView.as_view(), name='classroom_list_by_tag'),
    path('<uuid:pk>/', ClassroomDetailView.as_view(), name='classroom_detail'),
    path('<uuid:pk>/update/', ClassroomUpdate.as_view(), name='classroom_update'),
    path('<uuid:pk>/delete/', ClassroomDelete.as_view(), name='classroom_delete'),
    path('<uuid:pk>/people/', ClassroomPeopleView.as_view(), name='classroom_people'),
    path('create/', ClassroomCreate.as_view(), name='classroom_create'),
    path('enroll/', EnrollmentCreate.as_view(), name='enroll'),
    path('enroll/<uuid:pk>/delete/', EnrollmentDelete.as_view(), name='enroll_delete'),
]
