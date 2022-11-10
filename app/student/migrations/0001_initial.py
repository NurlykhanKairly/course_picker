# Generated by Django 4.0.6 on 2022-11-10 08:06

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('department', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Student',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=150)),
                ('student_id', models.CharField(max_length=20)),
                ('email', models.CharField(max_length=50)),
                ('username', models.CharField(max_length=20)),
                ('password', models.CharField(max_length=20)),
                ('year', models.IntegerField(choices=[(1, 'Freshman'), (2, 'Sophomore'), (3, 'Junior'), (4, 'Senior'), (5, 'Extension')], default=1)),
                ('major', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='student_main_major', to='department.department', verbose_name='Student Major Department')),
                ('minor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='student_minor', to='department.department', verbose_name='Student Minor Department')),
                ('second_major', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='student_second_major', to='department.department', verbose_name='Student Second Major Department')),
            ],
            options={
                'verbose_name': 'KAIST Student',
                'verbose_name_plural': 'KAIST Students',
            },
        ),
    ]
