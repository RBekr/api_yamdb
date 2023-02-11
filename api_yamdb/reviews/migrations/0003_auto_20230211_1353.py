# Generated by Django 3.2 on 2023-02-11 06:53

import api.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='score',
            field=models.IntegerField(validators=[api.validators.validate_score], verbose_name='Оценка'),
        ),
        migrations.AlterField(
            model_name='title',
            name='year',
            field=models.PositiveIntegerField(validators=[api.validators.title_year_validator], verbose_name='Год публикации'),
        ),
    ]
