# Generated by Django 3.2 on 2022-09-07 12:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_author_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='author',
            name='title',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='author',
            name='profile',
            field=models.TextField(blank=True, null=True),
        ),
    ]
