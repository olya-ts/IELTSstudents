# Generated by Django 4.0.2 on 2022-02-14 07:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ielts', '0002_student_package'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='curator',
            options={'ordering': ['name']},
        ),
        migrations.AlterModelOptions(
            name='student',
            options={'ordering': ['course', 'last_name']},
        ),
    ]
