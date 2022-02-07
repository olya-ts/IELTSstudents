from django.urls import path
from . import views


urlpatterns = [
    path('course20/', views.display_course20),
    path('course21/', views.display_course21),
    path('course22/', views.display_course22)
]
