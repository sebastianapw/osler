# Generated by Django 3.1.2 on 2020-12-22 02:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_auto_20201221_2024'),
        ('followup', '0003_auto_20201202_1250'),
    ]

    operations = [
        migrations.AlterField(
            model_name='actionitemfollowup',
            name='action_item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.actionitem', verbose_name='Action item'),
        ),
        migrations.AlterField(
            model_name='actionitemfollowup',
            name='contact_method',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='core.contactmethod', verbose_name='Contact method'),
        ),
        migrations.AlterField(
            model_name='actionitemfollowup',
            name='contact_resolution',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='followup.contactresult', verbose_name='Contact resolution'),
        ),
        migrations.AlterField(
            model_name='contactresult',
            name='attempt_again',
            field=models.BooleanField(default=False, help_text='True if outcome means the pt should be contacted again.', verbose_name='Attempt again'),
        ),
        migrations.AlterField(
            model_name='contactresult',
            name='patient_reached',
            field=models.BooleanField(default=True, help_text='True if outcome means they reached the patient', verbose_name='Patient reached'),
        ),
        migrations.AlterField(
            model_name='historicalactionitemfollowup',
            name='action_item',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='core.actionitem', verbose_name='Action item'),
        ),
        migrations.AlterField(
            model_name='historicalactionitemfollowup',
            name='contact_method',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='core.contactmethod', verbose_name='Contact method'),
        ),
        migrations.AlterField(
            model_name='historicalactionitemfollowup',
            name='contact_resolution',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='followup.contactresult', verbose_name='Contact resolution'),
        ),
    ]