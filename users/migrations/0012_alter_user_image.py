# Generated by Django 5.0.6 on 2024-05-17 14:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0011_remove_diagnostik_patient_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='image',
            field=models.ImageField(blank=True, default='default.svg', null=True, upload_to='users-images/%Y/%m/%d/'),
        ),
    ]
