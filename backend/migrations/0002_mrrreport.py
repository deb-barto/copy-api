# Generated by Django 5.0.3 on 2024-03-23 05:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MRRReport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_generated', models.DateTimeField(auto_now_add=True)),
                ('data', models.JSONField()),
            ],
        ),
    ]