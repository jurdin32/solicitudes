# Generated by Django 4.0.3 on 2022-04-09 15:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Permisos', '0006_alter_solicitudpermiso_cantidad_horas'),
    ]

    operations = [
        migrations.CreateModel(
            name='Anios',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('anio', models.IntegerField(default=2022)),
            ],
        ),
    ]
