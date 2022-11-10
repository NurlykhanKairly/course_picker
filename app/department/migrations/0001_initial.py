# Generated by Django 4.0.6 on 2022-11-10 08:06

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Department',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('id', models.IntegerField()),
                ('code', models.CharField(max_length=10)),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='DepartmentRequirements',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('credit', models.IntegerField()),
                ('major_mandatory', models.IntegerField()),
                ('elective_major', models.IntegerField()),
                ('type', models.IntegerField(choices=[(0, 'Major'), (1, 'Second Major'), (2, 'Minor')], default=0)),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='department.department')),
            ],
        ),
    ]