from rest_framework_nested import routers
from . import views

router = routers.DefaultRouter()

router.register('students', views.StudentViewSet, basename='students')
router.register('curators', views.CuratorViewSet, basename='curators')
router.register('teachers', views.TeacherViewSet, basename='teachers')
router.register('group_sessions', views.GroupSessionViewSet, basename='group_sessions')

teachers_router = routers.NestedDefaultRouter(router, 'teachers', lookup='teacher')
teachers_router.register('reviews', views.ReviewViewSet, basename='teacher-reviews')

urlpatterns = router.urls + teachers_router.urls
