# Generated by Django 4.1.1 on 2023-05-18 14:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Qalamy', '0004_myaudio'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myaudio',
            name='audio',
            field=models.FileField(blank=True, upload_to='qrcodes/'),
        ),
    ]
