# Generated by Django 4.0.3 on 2022-03-21 12:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ielts', '0008_remove_groupsession_teacher'),
    ]

    operations = [
        migrations.AddField(
            model_name='groupsession',
            name='teacher',
            field=models.ManyToManyField(related_name='groupsessions', to='ielts.teacher'),
        ),
    ]
