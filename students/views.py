from rest_framework.viewsets import ModelViewSet
from .models import Curator, Student
from .serializers import StudentSerializer, CuratorSerializer


class CuratorViewSet(ModelViewSet):
    queryset = Curator.objects.all()
    serializer_class = CuratorSerializer


class Course20ViewSet(ModelViewSet):
    queryset = Student.objects.filter(course=20).select_related('curator').all()
    serializer_class = StudentSerializer


class Course21ViewSet(ModelViewSet):
    queryset = Student.objects.filter(course=21).select_related('curator').all()
    serializer_class = StudentSerializer


class Course22ViewSet(ModelViewSet):
    queryset = Student.objects.filter(course=21).select_related('curator').all()
    serializer_class = StudentSerializer
