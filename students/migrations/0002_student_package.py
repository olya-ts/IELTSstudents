# Generated by Django 4.0.2 on 2022-02-09 10:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ielts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='package',
            field=models.CharField(choices=[('B', 'Basic'), ('S', 'Standard'), ('V', 'VIP')], default='S', max_length=10),
        ),
    ]
