# Generated by Django 4.2.2 on 2024-04-16 18:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('register', '0004_alter_child_middle_name_alter_childimage_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='child',
            name='gender',
            field=models.CharField(blank=True, choices=[('Boy', 'Boy'), ('Girl', 'Girl')], max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='parent',
            name='home_county',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='parent',
            name='phone_number',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
