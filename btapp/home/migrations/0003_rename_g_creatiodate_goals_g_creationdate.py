# Generated by Django 5.1.3 on 2024-11-12 19:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_goals'),
    ]

    operations = [
        migrations.RenameField(
            model_name='goals',
            old_name='g_creatioDate',
            new_name='g_creationDate',
        ),
    ]
