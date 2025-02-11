# Generated by Django 5.0.6 on 2024-05-19 12:43

import users.utils
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0017_user_diagnos_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='image',
            field=models.ImageField(blank=True, default='default.svg', null=True, upload_to='users-images/%Y/%m/%d/', validators=[users.utils.validate_image]),
        ),
    ]
