# Generated by Django 4.2.4 on 2023-08-28 04:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_user_is_registration_completed'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='profile_picture',
            field=models.URLField(blank=True, null=True),
        ),
    ]