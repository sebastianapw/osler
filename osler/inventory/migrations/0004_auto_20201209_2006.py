# Generated by Django 3.1.2 on 2020-12-10 02:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0003_dispensehistory_encounter'),
        ('core','0007_make_encounters'),
    ]

    operations = [
    	migrations.AlterField(
            model_name='dispensehistory',
            name='encounter',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.encounter'),
        ),
    ]
