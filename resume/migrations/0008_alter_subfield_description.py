# Generated by Django 4.0.3 on 2022-05-10 08:50

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('resume', '0007_resume_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subfield',
            name='description',
            field=ckeditor.fields.RichTextField(),
        ),
    ]