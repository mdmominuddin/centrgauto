# Generated by Django 4.2.10 on 2024-03-12 16:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0004_upevent'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='upevent',
            name='description',
        ),
    ]
