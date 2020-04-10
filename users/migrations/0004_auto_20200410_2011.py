# Generated by Django 3.0.5 on 2020-04-10 11:11

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0003_auto_20200410_1932"),
    ]

    operations = [
        migrations.RenameField(
            model_name="user", old_name="email_confirmed", new_name="email_verified",
        ),
        migrations.AddField(
            model_name="user",
            name="email_secret",
            field=models.CharField(blank=True, default="", max_length=120),
        ),
    ]