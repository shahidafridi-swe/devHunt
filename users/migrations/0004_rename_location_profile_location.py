# Generated by Django 4.2.1 on 2023-05-14 18:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_profile_location_skill'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='Location',
            new_name='location',
        ),
    ]