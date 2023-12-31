# Generated by Django 3.2.19 on 2023-07-23 14:24

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='WhiteList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('app_name', models.CharField(max_length=256)),
                ('version', models.CharField(max_length=256)),
                ('ip_addr', models.CharField(max_length=256)),
            ],
            options={
                'unique_together': {('app_name', 'version', 'ip_addr')},
            },
        ),
        migrations.CreateModel(
            name='UnauthorizedApp',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('app_name', models.CharField(max_length=256)),
                ('reason', models.CharField(max_length=256)),
                ('ip_addr', models.CharField(max_length=256)),
                ('install_date', models.CharField(max_length=256)),
            ],
            options={
                'unique_together': {('app_name', 'ip_addr')},
            },
        ),
    ]
