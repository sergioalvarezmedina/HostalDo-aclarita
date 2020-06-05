# Generated by Django 3.0.6 on 2020-05-25 20:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hostalapp', '0002_auto_20200515_1809'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ayuda',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=200)),
                ('subtitulo', models.CharField(max_length=200)),
                ('contenido', models.TextField()),
                ('creado', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')),
                ('modificado', models.DateTimeField(auto_now=True, verbose_name='Fecha de modificación')),
            ],
        ),
    ]
