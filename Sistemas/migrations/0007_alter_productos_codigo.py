# Generated by Django 5.0.4 on 2024-11-08 03:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Sistemas', '0006_alter_productos_microdescripcion'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productos',
            name='Codigo',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]