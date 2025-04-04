# Generated by Django 5.1.5 on 2025-04-01 17:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0004_feedback'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='logical_score',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='student',
            name='numerical1_score',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='student',
            name='numerical_score',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='student',
            name='reasoning_score',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='student',
            name='spatial_score',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='student',
            name='verbal_score',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
