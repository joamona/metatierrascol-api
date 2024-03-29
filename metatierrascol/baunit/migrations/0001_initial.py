# Generated by Django 4.2.7 on 2024-02-14 10:05

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Baunit',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('fecha_creacion', models.DateTimeField(auto_now=True)),
                ('codigo_acceso', models.UUIDField(blank=True, default=uuid.uuid4, editable=False, unique=True)),
                ('nombre', models.TextField(max_length=100)),
                ('numero_predial', models.TextField(blank=True, max_length=50)),
                ('complemento', models.TextField(help_text='Complemento de la dirección para ayudar a localizar el predio', max_length=200)),
                ('longitud', models.FloatField(blank=True, help_text='Longitud del punto central del predio')),
                ('latitud', models.FloatField(blank=True, help_text='Latitud del punto central del predio')),
                ('numero_catastral', models.TextField(blank=True, max_length=30)),
            ],
            options={
                'db_table': 'baunit"."baunit',
                'managed': False,
            },
        ),
    ]
