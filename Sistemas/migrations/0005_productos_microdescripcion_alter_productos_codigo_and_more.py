# Generated by Django 5.0.4 on 2024-10-26 02:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Sistemas', '0004_delete_contacto'),
    ]

    operations = [
        migrations.AddField(
            model_name='productos',
            name='MicroDescripcion',
            field=models.TextField(default='Descripción predeterminada', max_length=100),
        ),
        migrations.AlterField(
            model_name='productos',
            name='Codigo',
            field=models.IntegerField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='productos',
            name='Descripcion',
            field=models.TextField(),
        ),
    ]
