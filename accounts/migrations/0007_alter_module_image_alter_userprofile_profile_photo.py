# Generated by Django 5.0.2 on 2024-03-04 07:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_remove_module_file_module_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='module',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='module_media/'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='profile_photo',
            field=models.FileField(blank=True, null=True, upload_to='user_media/'),
        ),
    ]