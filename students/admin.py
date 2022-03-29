from datetime import datetime, date
from django.db.models.query import QuerySet
from django.db.models.aggregates import Count
from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html, urlencode
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
    autocomplete_fields = ['curator']
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


class StudentInline(admin.StackedInline):
    model = models.Student
    extra = 0


@admin.register(models.Curator)
class CuratorAdmin(admin.ModelAdmin):
    inlines = [StudentInline]
    list_display = ['name', 'phone', 'student_count']
    search_fields = ['name__istartswith']

    @admin.display(ordering='student_count')
    def student_count(self, curator):
        url = (
            reverse('admin:students_student_changelist')
            + '?'
            + urlencode({
                'curator__id': str(curator.id)
            }))
        return format_html('<a href="{}">{}</a>', url, curator.student_count)

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(student_count=Count('student__id'))


@admin.register(models.Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'phone', 'email', 'skype_name', 'about_me']
    list_editable = ['phone', 'skype_name', 'about_me']
    search_fields = ['first_name__istartswith', 'last_name__istartswith']


@admin.register(models.GroupSession)
class GroupSessionAdmin(admin.ModelAdmin):
    list_display = ['title', 'description']
    list_editable = ['description']
    search_fields = ['title__istartswith']

    # def teachers(self, obj):
    #     return ", ".join([t.first_name for t in obj.teacher.all()])
