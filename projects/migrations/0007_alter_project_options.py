# Generated by Django 4.2.1 on 2023-05-20 19:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0006_alter_project_options_review_owner_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='project',
            options={'ordering': ['-vote_total', '-vote_ratio', 'title']},
        ),
    ]
