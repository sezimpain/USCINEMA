# Generated by Django 3.2.7 on 2022-02-03 09:09

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('film', '0002_auto_20220203_0839'),
    ]

    operations = [
        migrations.AlterField(
            model_name='videoreview',
            name='rating',
            field=models.PositiveIntegerField(default=1, validators=[django.core.validators.MaxValueValidator(5)]),
        ),
    ]
