from datetime import datetime, date
from django.db.models.query import QuerySet
from django.contrib import admin
from . import models


class StudentStatusFilter(admin.SimpleListFilter):
    title = 'student_status'
    parameter_name = 'student_status'

    def lookups(self, request, model_admin):
        return [
            ('< datetime.date(datetime.now()', 'FINISHED'),
            ('< date(2022, 4, 30)', 'URGENT'),
            ('>= date(2022, 4, 30)', 'REGULAR')
        ]

    def queryset(self, request, queryset: QuerySet):
        if self.value() == '< datetime.date(datetime.now()':
            return queryset.filter(exam_date__lt=datetime.date(datetime.now()))
        if self.value() == '< date(2022, 4, 30)':
            return queryset.filter(exam_date__lt=date(2022, 4, 30), exam_date__gte=datetime.date(datetime.now()))
        if self.value() == '>= date(2022, 4, 30)':
            return queryset.filter(exam_date__gte=date(2022, 4, 30))


@admin.register(models.Student)
class StudentAdmin(admin.ModelAdmin):
    list_editable = [
        'first_name',
        'last_name',
        'exam_date',
        'package'
    ]
    list_display = [
        'course',
        'curator',
        'first_name',
        'last_name',
        'phone',
        'email',
        'skype_name',
        'ielts_module',
        'goal_score',
        'exam_date',
        'package',
        'urgent_students'
    ]
    list_filter = ['course', 'curator', StudentStatusFilter]
    list_per_page = 20
    search_fields = ['last_name__istartswith', 'phone']

    @admin.display(ordering='exam_date')
    def urgent_students(self, student):
        if student.exam_date < datetime.date(datetime.now()):
            return "FINISHED"
        elif student.exam_date < date(2022, 4, 30):
            return "URGENT"
        return "REGULAR"
