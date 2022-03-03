from rest_framework import serializers
from .models import Student, Curator


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
