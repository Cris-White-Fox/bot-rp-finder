# Generated by Django 4.0.6 on 2022-12-26 10:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0003_alter_interaction_unique_together'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='last_activity',
            field=models.DateTimeField(auto_now_add=True, null=True, verbose_name='Дата последней активности'),
        ),
    ]
