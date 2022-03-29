from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from .models import Curator, Student, Teacher, GroupSession, Review
from .serializers import StudentSerializer, CuratorSerializer, TeacherSerializer, GroupSessionSerializer, \
    ReviewSerializer
from .pagination import DefaultPagination


class CuratorViewSet(ModelViewSet):
    queryset = Curator.objects.all()
    serializer_class = CuratorSerializer
    filter_backends = [SearchFilter]
    search_fields = ['name']


class StudentViewSet(ModelViewSet):
    serializer_class = StudentSerializer
    filter_backends = [OrderingFilter]
    ordering_fields = ['first_name', 'last_name', 'course']
    pagination_class = DefaultPagination

    def get_queryset(self):
        queryset = Student.objects.select_related('curator').all()
        course = self.request.query_params.get('course')
        if course is not None:
            queryset = Student.objects.filter(course=course).select_related('curator').all()
        return queryset


class TeacherViewSet(ModelViewSet):
    queryset = Teacher.objects.prefetch_related('groupsessions').all()
    serializer_class = TeacherSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['groupsessions']
    search_fields = ['first_name', 'last_name']
    ordering_fields = ['first_name', 'last_name']


class GroupSessionViewSet(ModelViewSet):
    queryset = GroupSession.objects.prefetch_related('teacher').all()
    serializer_class = GroupSessionSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['teacher']
    search_fields = ['title']
    ordering_fields = ['title']


class ReviewViewSet(ModelViewSet):

    serializer_class = ReviewSerializer

    def get_queryset(self):
        return Review.objects.filter(teacher_id=self.kwargs['teacher_pk'])

    def get_serializer_context(self):
        return {'teacher_id': self.kwargs['teacher_pk']}
