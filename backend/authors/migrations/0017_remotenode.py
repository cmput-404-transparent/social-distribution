# Generated by Django 5.1.2 on 2024-11-03 21:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authors', '0016_siteconfiguration_delete_sitesettings'),
    ]

    operations = [
        migrations.CreateModel(
            name='RemoteNode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.URLField(unique=True)),
                ('username', models.CharField(max_length=250)),
                ('token', models.CharField(blank=True, max_length=250, null=True)),
            ],
        ),
    ]
