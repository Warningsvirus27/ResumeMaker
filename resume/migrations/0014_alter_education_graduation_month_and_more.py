# Generated by Django 4.0.3 on 2022-05-12 10:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resume', '0013_education_suffix'),
    ]

    operations = [
        migrations.AlterField(
            model_name='education',
            name='graduation_month',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='education',
            name='graduation_year',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
