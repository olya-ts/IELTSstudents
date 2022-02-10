from django.shortcuts import render
from students.models import Curator, Student


def display_course20(request):
    query_set = Student.objects.\
        values_list(
            'curator__name',
            'first_name',
            'last_name',
            'phone',
            'email',
            'skype_name',
            'ielts_module',
            'goal_score',
            'exam_date') \
        .filter(course=20) \
        .order_by('curator__name', 'first_name', 'last_name')
    return render(request, 'course20.html', {'course20': list(query_set)})


def display_course21(request):
    query_set = Student.objects.\
        values_list(
            'curator__name',
            'first_name',
            'last_name',
            'phone',
            'email',
            'skype_name',
            'ielts_module',
            'goal_score',
            'exam_date') \
        .filter(course=21) \
        .order_by('curator__name', 'first_name', 'last_name')
    return render(request, 'course21.html', {'course21': list(query_set)})


def display_course22(request):
    query_set = Student.objects.\
        values_list(
            'curator__name',
            'first_name',
            'last_name',
            'phone',
            'email',
            'skype_name',
            'ielts_module',
            'goal_score',
            'exam_date') \
        .filter(course=22) \
        .order_by('curator__name', 'first_name', 'last_name')
    return render(request, 'course22.html', {'course22': list(query_set)})
