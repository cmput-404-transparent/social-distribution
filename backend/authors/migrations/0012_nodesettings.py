# Generated by Django 5.1.2 on 2024-11-02 17:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authors', '0011_author_is_approved'),
    ]

    operations = [
        migrations.CreateModel(
            name='NodeSettings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('approval_required', models.BooleanField(default=True)),
            ],
        ),
    ]
