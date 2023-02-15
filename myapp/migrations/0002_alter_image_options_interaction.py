# Generated by Django 4.0.6 on 2022-12-26 06:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='image',
            options={'verbose_name': 'Изображение анкеты', 'verbose_name_plural': 'Изображения анкет'},
        ),
        migrations.CreateModel(
            name='Interaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('result', models.BooleanField(verbose_name='Результат взаимодействия')),
                ('datetime', models.DateTimeField(auto_now_add=True, verbose_name='Дата взаимодействия')),
                ('initiator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='interaction_initiator', to='myapp.profile', verbose_name='Инициатор')),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='interaction_subject', to='myapp.profile', verbose_name='Субъект')),
            ],
            options={
                'verbose_name': 'Взаимодействие пользователей',
                'verbose_name_plural': 'Взаимодействия пользователей',
            },
        ),
    ]
