# Generated by Django 2.1.7 on 2019-03-28 13:52

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_like'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='user',
            field=models.ForeignKey(null=True, on_delete='CASCADE', to=settings.AUTH_USER_MODEL),
        ),
    ]
