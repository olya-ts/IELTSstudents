from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from .models import Curator, Student, Teacher, GroupSession
from .serializers import StudentSerializer, CuratorSerializer, TeacherSerializer, GroupSessionSerializer


class CuratorViewSet(ModelViewSet):
    queryset = Curator.objects.all()
    serializer_class = CuratorSerializer
    filter_backends = [SearchFilter]
    search_fields = ['name']


class StudentViewSet(ModelViewSet):
    serializer_class = StudentSerializer

    def get_queryset(self):
        queryset = Student.objects.select_related('curator').all()
        course = self.request.query_params.get('course')
        if course is not None:
            queryset = Student.objects.filter(course=course).select_related('curator').all()
        return queryset


class TeacherViewSet(ModelViewSet):
    queryset = Teacher.objects.prefetch_related('groupsessions').all()
    serializer_class = TeacherSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['groupsessions']
    search_fields = ['first_name', 'last_name']


class GroupSessionViewSet(ModelViewSet):
    queryset = GroupSession.objects.prefetch_related('teacher').all()
    serializer_class = GroupSessionSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['teacher']
    search_fields = ['title']
