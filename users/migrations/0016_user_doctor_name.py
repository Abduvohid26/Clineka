# Generated by Django 5.0.6 on 2024-05-19 05:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0015_remove_patient_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='doctor_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
