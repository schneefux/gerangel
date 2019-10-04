# Generated by Django 2.2.1 on 2019-10-04 15:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('matchlog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='match',
            name='owner',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='matches', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
