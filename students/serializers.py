from rest_framework import serializers
from .models import Student, Curator, Teacher, GroupSession, Review


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


class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = ['id', 'first_name', 'last_name', 'phone', 'email', 'skype_name', 'about_me', 'groupsessions']


class GroupSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupSession
        fields = ['id', 'title', 'description', 'teacher']


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'name', 'description', 'date']

    def create(self, validated_data):
        teacher_id = self.context['teacher_id']
        return Review.objects.create(teacher_id=teacher_id, **validated_data)
