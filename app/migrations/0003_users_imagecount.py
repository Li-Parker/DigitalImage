# Generated by Django 4.2 on 2023-05-31 14:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0002_alter_images_img"),
    ]

    operations = [
        migrations.AddField(
            model_name="users",
            name="imageCount",
            field=models.IntegerField(default=0, verbose_name="上传照片数量"),
        ),
    ]
