# Generated by Django 4.2.7 on 2024-02-25 10:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('proyecto', '0011_cronconfig'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cronconfig',
            name='dia_mes',
        ),
        migrations.RemoveField(
            model_name='cronconfig',
            name='hora',
        ),
        migrations.RemoveField(
            model_name='cronconfig',
            name='mes',
        ),
        migrations.RemoveField(
            model_name='cronconfig',
            name='minuto',
        ),
        migrations.AddField(
            model_name='cronconfig',
            name='hora_ejecucion',
            field=models.CharField(default='00:00', max_length=5),
        ),
        migrations.AlterField(
            model_name='cronconfig',
            name='dia_semana',
            field=models.CharField(default='*', max_length=3),
        ),
    ]