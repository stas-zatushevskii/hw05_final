# Generated by Django 2.2.16 on 2021-09-02 15:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0007_auto_20210902_1833'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='text',
            field=models.TextField(help_text='Введите текст коментария', verbose_name='Текст коментария'),
        ),
    ]
