# Generated by Django 5.1.2 on 2024-10-31 03:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authors', '0008_alter_author_host_alter_author_page'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='password',
            field=models.CharField(max_length=100),
        ),
    ]