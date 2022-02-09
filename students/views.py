from django.shortcuts import render
from students.models import Curator, Student


def display_course20(request):
    query_set = Student.objects.filter()
    return render(request, 'course20.html')


def display_course21(request):
    return render(request, 'course21.html')


def display_course22(request):
    return render(request, 'course22.html')
