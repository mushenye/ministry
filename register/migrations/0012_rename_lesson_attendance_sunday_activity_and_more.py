# Generated by Django 4.2.2 on 2024-04-18 17:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('register', '0011_sundayactivity_on_date'),
    ]

    operations = [
        migrations.RenameField(
            model_name='attendance',
            old_name='lesson',
            new_name='sunday_activity',
        ),
        migrations.AddField(
            model_name='attendance',
            name='in_attendance',
            field=models.BooleanField(default=False),
        ),
    ]
