# Generated by Django 3.0.4 on 2020-03-22 06:42

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("rooms", "0007_auto_20200321_2220"),
    ]

    operations = [
        migrations.AlterField(
            model_name="photo",
            name="file",
            field=models.ImageField(upload_to="room_photos"),
        ),
    ]