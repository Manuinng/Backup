# Generated by Django 4.2.7 on 2023-11-27 01:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('proyecto', '0007_alter_detalle_backup_id_backup_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='detalle_backup',
            name='contenido',
            field=models.FileField(blank=True, null=True, upload_to=''),
        ),
    ]
