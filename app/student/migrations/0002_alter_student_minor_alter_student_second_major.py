# Generated by Django 4.0.6 on 2022-11-10 08:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('department', '0001_initial'),
        ('student', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='minor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='student_minor', to='department.department', verbose_name='Student Minor Department'),
        ),
        migrations.AlterField(
            model_name='student',
            name='second_major',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='student_second_major', to='department.department', verbose_name='Student Second Major Department'),
        ),
    ]
