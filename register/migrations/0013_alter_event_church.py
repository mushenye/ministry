# Generated by Django 5.0.4 on 2024-05-08 11:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('register', '0012_alter_orderofevent_local_church'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='church',
            field=models.CharField(max_length=20),
        ),
    ]
