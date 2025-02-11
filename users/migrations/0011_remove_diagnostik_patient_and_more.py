# Generated by Django 5.0.6 on 2024-05-17 14:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0010_diagnostik'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='diagnostik',
            name='patient',
        ),
        migrations.RemoveField(
            model_name='recommendation',
            name='patient',
        ),
        migrations.AddField(
            model_name='user',
            name='complaint',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='diagnostik_cure',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='diagnostik_name',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='image',
            field=models.ImageField(default='', upload_to=''),
        ),
        migrations.AddField(
            model_name='user',
            name='recommendation',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.DeleteModel(
            name='Complaint',
        ),
        migrations.DeleteModel(
            name='Diagnostik',
        ),
        migrations.DeleteModel(
            name='Recommendation',
        ),
    ]
