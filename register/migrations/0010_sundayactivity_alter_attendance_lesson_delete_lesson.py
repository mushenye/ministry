# Generated by Django 4.2.2 on 2024-04-18 08:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('register', '0009_alter_child_gender_alter_parent_home_county'),
    ]

    operations = [
        migrations.CreateModel(
            name='SundayActivity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateField(auto_now_add=True)),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField(max_length=200)),
                ('children_attendance', models.ManyToManyField(related_name='lessons_attended', through='register.Attendance', to='register.child')),
            ],
        ),
        migrations.AlterField(
            model_name='attendance',
            name='lesson',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='register.sundayactivity'),
        ),
        migrations.DeleteModel(
            name='Lesson',
        ),
    ]