from django.db import migrations, models
import uuid

class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0003_post_github_activity_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='id',
        ),
        migrations.AddField(
            model_name='post',
            name='id',
            field=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False),
        ),
        migrations.RemoveField(
            model_name='share',
            name='id',
        ),
        migrations.AddField(
            model_name='share',
            name='id',
            field=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False),
        ),
    ]
