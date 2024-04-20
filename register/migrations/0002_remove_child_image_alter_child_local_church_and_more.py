# Generated by Django 4.2.2 on 2024-04-15 14:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('register', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='child',
            name='image',
        ),
        migrations.AlterField(
            model_name='child',
            name='local_church',
            field=models.CharField(choices=[('South B', 'South B'), ('Kiambiu', 'Kiambiu'), ('Kitengela', 'Kitengela'), ('Waudo', 'Waudo'), ('Eastleigh', 'Eastleigh'), ('Umoja', 'Umoja'), ('Muthaiga', 'Muthaiga'), ('Runda', 'Runda'), ('Kariokor', 'Kariokor')], max_length=100),
        ),
        migrations.CreateModel(
            name='ChildImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateField(auto_now_add=True)),
                ('image', models.ImageField(upload_to='child_images')),
                ('child', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='register.child')),
            ],
        ),
    ]
