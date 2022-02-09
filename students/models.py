from django.db import models


class Curator(models.Model):
    name = models.CharField(max_length=30)
    phone = models.CharField(max_length=40, unique=True)


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

    course = models.IntegerField()
    curator = models.ForeignKey(Curator, on_delete=models.PROTECT)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=30)
    phone = models.CharField(max_length=40, unique=True)
    email = models.EmailField(unique=True)
    skype_name = models.CharField(max_length=40)
    ielts_module = models.CharField(
        max_length=10,
        verbose_name='IELTS Module',
        choices=MODULE_CHOICES,
        default=MODULE_GENERAL
    )
    goal_score = models.DecimalField(max_digits=2, decimal_places=1)
    exam_date = models.DateField(null=True)
    package = models.CharField(max_length=10, choices=PACKAGE_CHOICES, default=PACKAGE_STANDARD)
