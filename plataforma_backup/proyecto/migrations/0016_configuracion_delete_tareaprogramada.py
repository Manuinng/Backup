# Generated by Django 4.2.7 on 2024-03-03 08:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('proyecto', '0015_tareaprogramada'),
    ]

    operations = [
        migrations.CreateModel(
            name='Configuracion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hora_respaldo', models.TimeField()),
            ],
        ),
        migrations.DeleteModel(
            name='TareaProgramada',
        ),
    ]
