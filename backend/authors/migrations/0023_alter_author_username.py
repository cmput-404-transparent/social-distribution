# Generated by Django 5.1.2 on 2024-11-24 01:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authors', '0022_merge_20241124_0106'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='username',
            field=models.CharField(max_length=250, unique=True),
        ),
    ]
