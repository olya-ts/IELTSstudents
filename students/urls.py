from rest_framework.routers import DefaultRouter
from django.urls import path
from . import views

router = DefaultRouter()

router.register('students', views.StudentViewSet, basename='students')
router.register('curators', views.CuratorViewSet, basename='curators')
router.register('teachers', views.TeacherViewSet, basename='teachers')
router.register('group_sessions', views.GroupSessionViewSet, basename='group_sessions')

urlpatterns = router.urls
