# Generated by Django 5.0.7 on 2024-07-20 13:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0007_alter_results_id_alter_results_unique_together'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='staffs',
            name='address',
        ),
        migrations.RemoveField(
            model_name='students',
            name='address',
        ),
        migrations.AddField(
            model_name='customuser',
            name='address',
            field=models.TextField(default='na'),
            preserve_default=False,
        ),
    ]
