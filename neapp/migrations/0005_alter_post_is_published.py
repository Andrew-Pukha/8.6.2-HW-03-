# Generated by Django 4.2.1 on 2024-11-30 15:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('neapp', '0004_alter_post_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='is_published',
            field=models.BooleanField(choices=[(0, 'Черновик'), (1, 'Опубликовано')], default=1),
        ),
    ]