# Generated by Django 4.0.2 on 2022-02-07 13:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Curator',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('phone', models.CharField(max_length=40, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course', models.IntegerField()),
                ('first_name', models.CharField(max_length=20)),
                ('last_name', models.CharField(max_length=30)),
                ('phone', models.CharField(max_length=40, unique=True)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('skype_name', models.CharField(max_length=40)),
                ('ielts_module', models.CharField(choices=[('G', 'General'), ('A', 'Academic')], default='G', max_length=10, verbose_name='IELTS Module')),
                ('goal_score', models.DecimalField(decimal_places=1, max_digits=2)),
                ('exam_date', models.DateField(null=True)),
                ('curator', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='students.curator')),
            ],
        ),
    ]
