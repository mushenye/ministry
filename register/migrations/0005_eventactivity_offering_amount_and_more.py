# Generated by Django 5.0.4 on 2024-05-07 05:04

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('register', '0004_remove_orderofevent_events_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='eventactivity',
            name='offering_amount',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='eventactivity',
            name='tithe_amount',
            field=models.IntegerField(default=10),
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateField(auto_now_add=True)),
                ('church', models.CharField(choices=[('South B', 'South B'), ('Kiambiu', 'Kiambiu'), ('Kitengela', 'Kitengela'), ('Waudo', 'Waudo'), ('Eastleigh', 'Eastleigh'), ('Umoja', 'Umoja'), ('Muthaiga', 'Muthaiga'), ('Runda', 'Runda'), ('Kariokor', 'Kariokor'), ('KMM', 'KMM')], max_length=20)),
                ('event', models.CharField(choices=[], max_length=100)),
                ('associate', models.CharField(max_length=100)),
                ('calendar', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='register.calenderevent')),
            ],
        ),
        migrations.AddField(
            model_name='eventactivity',
            name='event',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='register.event'),
        ),
        migrations.CreateModel(
            name='OrderOfEvent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateField(auto_now_add=True)),
                ('calendar', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='register.calenderevent')),
                ('events', models.ManyToManyField(related_name='events', through='register.EventActivity', to='register.event')),
            ],
        ),
        migrations.AddField(
            model_name='eventactivity',
            name='order_of_events',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='register.orderofevent'),
        ),
    ]