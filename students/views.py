from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework import status
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
    permission_classes = [IsAdminUser]
    http_method_names = ['get', 'post', 'put', 'patch', 'delete', 'head', 'options']

    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthenticated()]
        return [IsAdminUser()]

    def destroy(self, request, *args, **kwargs):
        if Student.objects.filter(curator_id=kwargs['pk']).count() > 0:
            return Response(
                {'error': 'Curator cannot be deleted as they are associated with students'},
                status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().destroy(request, *args, **kwargs)


class StudentViewSet(ModelViewSet):
    serializer_class = StudentSerializer
    filter_backends = [OrderingFilter]
    ordering_fields = ['first_name', 'last_name', 'course']
    pagination_class = DefaultPagination
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'post', 'put', 'patch', 'delete', 'head', 'options']

    def get_queryset(self):
        queryset = Student.objects.select_related('curator').all()
        course = self.request.query_params.get('course')
        if course is not None:
            queryset = Student.objects.filter(course=course).select_related('curator').all()
        return queryset

    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthenticated()]
        return [IsAdminUser()]


class TeacherViewSet(ModelViewSet):
    queryset = Teacher.objects.prefetch_related('groupsessions').all()
    serializer_class = TeacherSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['groupsessions']
    search_fields = ['first_name', 'last_name']
    ordering_fields = ['first_name', 'last_name']
    permission_classes = [IsAdminUser]
    http_method_names = ['get', 'post', 'put', 'patch', 'delete', 'head', 'options']

    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthenticated()]
        return [IsAdminUser()]


class GroupSessionViewSet(ModelViewSet):
    queryset = GroupSession.objects.prefetch_related('teacher').all()
    serializer_class = GroupSessionSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['teacher']
    search_fields = ['title']
    ordering_fields = ['title']
    permission_classes = [IsAdminUser]
    http_method_names = ['get', 'post', 'put', 'patch', 'delete', 'head', 'options']

    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthenticated()]
        return [IsAdminUser()]


class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'post', 'delete']

    def get_queryset(self):
        return Review.objects.filter(teacher_id=self.kwargs['teacher_pk'])

    def get_serializer_context(self):
        return {'teacher_id': self.kwargs['teacher_pk']}

    def get_permissions(self):
        if self.request.method == 'DELETE':
            return [IsAdminUser()]
        return [IsAuthenticated()]
