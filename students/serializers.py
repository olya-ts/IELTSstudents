from rest_framework import serializers
from .models import Student, Curator, Teacher, GroupSession


class CuratorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Curator
        fields = ['id', 'name', 'phone']


class StudentSerializer(serializers.ModelSerializer):
    curator = serializers.HyperlinkedRelatedField(
        queryset=Curator.objects.all(),
        view_name='curators-detail'
    )

    class Meta:
        model = Student
        fields = ['id', 'course', 'curator', 'first_name', 'last_name']


# class GroupSessionListingField(serializers.RelatedField):
#     def to_representation(self, value):
#         return value.title


class TeacherSerializer(serializers.ModelSerializer):
    # group_sessions = GroupSessionListingField(many=True, read_only=True)

    class Meta:
        model = Teacher
        fields = ['first_name', 'last_name', 'phone', 'email', 'skype_name', 'about_me']


class GroupSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupSession
        fields = ['title', 'description']
