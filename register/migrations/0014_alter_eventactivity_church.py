# Generated by Django 4.2.2 on 2024-04-20 09:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('register', '0013_calenderevent_eventactivity_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventactivity',
            name='church',
            field=models.CharField(choices=[('South B', 'South B'), ('Kiambiu', 'Kiambiu'), ('Kitengela', 'Kitengela'), ('Waudo', 'Waudo'), ('Eastleigh', 'Eastleigh'), ('Umoja', 'Umoja'), ('Muthaiga', 'Muthaiga'), ('Runda', 'Runda'), ('Kariokor', 'Kariokor'), ('KMM', 'KMM')], default='KMM', max_length=20),
        ),
    ]
