# Generated by Django 4.2.9 on 2024-01-05 11:04

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('notes', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='note',
            name='shared_with',
            field=models.ManyToManyField(related_name='shared_notes', to=settings.AUTH_USER_MODEL),
        ),
    ]
