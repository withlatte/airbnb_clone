# Generated by Django 3.0.4 on 2020-03-16 11:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("rooms", "0004_auto_20200315_2125"),
    ]

    operations = [
        migrations.RemoveField(model_name="photo", name="name",),
        migrations.AlterField(
            model_name="photo",
            name="file",
            field=models.ImageField(upload_to="uploads"),
        ),
        migrations.AlterField(
            model_name="photo",
            name="room",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="photos",
                to="rooms.Room",
            ),
        ),
    ]