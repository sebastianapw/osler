# Generated by Django 3.0.5 on 2020-09-10 20:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('demographics', '0003_auto_20200822_1458'),
    ]

    operations = [
        migrations.RenameField(
            model_name='demographics',
            old_name='chronic_condition',
            new_name='chronic_conditions',
        ),
    ]
