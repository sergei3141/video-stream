# Generated by Django 5.1.1 on 2024-10-03 10:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('upload', '0004_remove_videochunkedupload_completed_at_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='VideoChunkedUpload',
        ),
    ]
