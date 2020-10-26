# Generated by Django 3.1.2 on 2020-10-19 20:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appointment', '0002_auto_20200806_1411'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='pt_showed',
            field=models.BooleanField(blank=True, help_text='Did the patient come to this appointment?', null=True, verbose_name='Patient Showed'),
        ),
        migrations.AlterField(
            model_name='historicalappointment',
            name='pt_showed',
            field=models.BooleanField(blank=True, help_text='Did the patient come to this appointment?', null=True, verbose_name='Patient Showed'),
        ),
    ]