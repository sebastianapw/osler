# Generated by Django 2.0.13 on 2020-05-03 15:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('pttrack', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='PageviewRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_ip', models.GenericIPAddressField()),
                ('method', models.CharField(choices=[('GET', 'GET'), ('POST', 'POST'), ('HEAD', 'HEAD'), ('PUT', 'PUT'), ('PATCH', 'PATCH'), ('DELETE', 'DELETE'), ('CONNECT', 'CONNECT'), ('OPTIONS', 'OPTIONS'), ('TRACE', 'TRACE')], max_length=7)),
                ('url', models.URLField(max_length=256)),
                ('referrer', models.URLField(blank=True, max_length=256, null=True)),
                ('status_code', models.PositiveSmallIntegerField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('role', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='pttrack.ProviderType')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
