# Generated by Django 5.1.2 on 2024-10-20 05:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0002_alter_post_fqid'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='github_activity_id',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
