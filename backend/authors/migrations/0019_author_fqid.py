# Generated by Django 5.1.2 on 2024-11-12 19:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authors', '0018_alter_author_password'),
    ]

    operations = [
        migrations.AddField(
            model_name='author',
            name='fqid',
            field=models.URLField(blank=True, null=True),
        ),
    ]
