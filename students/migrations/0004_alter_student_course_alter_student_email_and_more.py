# Generated by Django 4.0.2 on 2022-02-14 10:38

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0003_alter_curator_options_alter_student_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='course',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(20)]),
        ),
        migrations.AlterField(
            model_name='student',
            name='email',
            field=models.EmailField(blank=True, max_length=254, unique=True, validators=[django.core.validators.EmailValidator]),
        ),
        migrations.AlterField(
            model_name='student',
            name='exam_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='goal_score',
            field=models.DecimalField(decimal_places=1, default=7.0, max_digits=2, validators=[django.core.validators.DecimalValidator(2, 1)]),
        ),
        migrations.AlterField(
            model_name='student',
            name='skype_name',
            field=models.CharField(blank=True, max_length=40),
        ),
    ]
