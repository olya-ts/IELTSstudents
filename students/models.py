from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, EmailValidator, DecimalValidator


class Curator(models.Model):
    name = models.CharField(max_length=30)
    phone = models.CharField(max_length=40, unique=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    objects = models.Manager()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Student(models.Model):
    MODULE_GENERAL = 'G'
    MODULE_ACADEMIC = 'A'
    MODULE_CHOICES = [
        (MODULE_GENERAL, 'General'),
        (MODULE_ACADEMIC, 'Academic')
    ]

    PACKAGE_BASIC = 'B'
    PACKAGE_STANDARD = 'S'
    PACKAGE_VIP = 'V'
    PACKAGE_CHOICES = [
        (PACKAGE_BASIC, 'Basic'),
        (PACKAGE_STANDARD, 'Standard'),
        (PACKAGE_VIP, 'VIP')
    ]

    course = models.IntegerField(validators=[MinValueValidator(20)])
    curator = models.ForeignKey(Curator, on_delete=models.PROTECT)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=30)
    phone = models.CharField(max_length=40, unique=True)
    email = models.EmailField(unique=True, blank=True, validators=[EmailValidator])
    skype_name = models.CharField(max_length=40, blank=True)
    ielts_module = models.CharField(
        max_length=10,
        verbose_name='IELTS Module',
        choices=MODULE_CHOICES,
        default=MODULE_GENERAL
    )
    goal_score = models.DecimalField(max_digits=2, decimal_places=1, default=7.0, validators=[DecimalValidator(2, 1)])
    exam_date = models.DateField(null=True, blank=True)
    package = models.CharField(max_length=10, choices=PACKAGE_CHOICES, default=PACKAGE_STANDARD)
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    objects = models.Manager()

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    class Meta:
        ordering = ['course', 'last_name']


class Teacher(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    phone = models.CharField(max_length=40, unique=True)
    email = models.EmailField(unique=True, blank=True, validators=[EmailValidator])
    skype_name = models.CharField(max_length=40, blank=True)
    about_me = models.TextField(null=True, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    objects = models.Manager()

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    class Meta:
        ordering = ['first_name', 'last_name']


class GroupSession(models.Model):
    title = models.CharField(max_length=40)
    description = models.TextField()
    teacher = models.ManyToManyField(Teacher, related_name='groupsessions')
    objects = models.Manager()

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['title']


class Review(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='reviews')
    name = models.CharField(max_length=50)
    description = models.TextField()
    date = models.DateField(auto_now_add=True)
    objects = models.Manager()
