from rest_framework.routers import SimpleRouter
from django.urls import path
from . import views

router = SimpleRouter()
router.register('course20', views.Course20ViewSet)
router.register('course21', views.Course21ViewSet)
router.register('course22', views.Course22ViewSet)
router.register('curators', views.CuratorViewSet, basename='curators')

urlpatterns = router.urls
