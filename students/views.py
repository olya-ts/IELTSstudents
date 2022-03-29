from rest_framework.viewsets import ModelViewSet
from .models import Curator, Student, Teacher, GroupSession
from .serializers import StudentSerializer, CuratorSerializer, TeacherSerializer, GroupSessionSerializer


class CuratorViewSet(ModelViewSet):
    queryset = Curator.objects.all()
    serializer_class = CuratorSerializer


class StudentViewSet(ModelViewSet):
    serializer_class = StudentSerializer

    def get_queryset(self):
        queryset = Student.objects.select_related('curator').all()
        course = self.request.query_params.get('course')
        if course is not None:
            queryset = Student.objects.filter(course=course).select_related('curator').all()
        return queryset


class TeacherViewSet(ModelViewSet):
    serializer_class = TeacherSerializer

    def get_queryset(self):
        queryset = Teacher.objects.prefetch_related('groupsessions').all()
        groupsession_id = self.request.query_params.get('groupsession_id')
        if groupsession_id is not None:
            queryset = Teacher.objects.filter(groupsessions=groupsession_id).prefetch_related('groupsessions').all()
        return queryset


class GroupSessionViewSet(ModelViewSet):
    serializer_class = GroupSessionSerializer

    def get_queryset(self):
        queryset = GroupSession.objects.prefetch_related('teacher').all()
        teacher_id = self.request.query_params.get('teacher_id')
        if teacher_id is not None:
            queryset = GroupSession.objects.filter(teacher=teacher_id).prefetch_related('teacher').all()
        return queryset
