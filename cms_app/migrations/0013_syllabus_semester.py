# Generated by Django 5.1.4 on 2025-03-04 04:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("cms_app", "0012_remove_syllabus_semester_alter_academicyear_name_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="syllabus",
            name="semester",
            field=models.CharField(default="Semester 1", max_length=20),
            preserve_default=False,
        ),
    ]
