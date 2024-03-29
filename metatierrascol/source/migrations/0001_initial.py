# Generated by Django 4.2.7 on 2024-02-14 10:05

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ArchivoZip',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('fecha_creacion', models.DateTimeField(auto_now=True)),
                ('fecha_descarga', models.DateTimeField(blank=True)),
                ('archivo', models.FileField(upload_to='ficheros_zip')),
                ('url_descarga', models.URLField(blank=True, max_length=400)),
            ],
            options={
                'db_table': 'source"."archivo_zip',
                'managed': False,
            },
        ),
    ]
