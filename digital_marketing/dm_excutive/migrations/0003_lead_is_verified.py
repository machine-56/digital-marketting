# Generated by Django 5.1.6 on 2025-04-27 23:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dm_excutive', '0002_remove_lead_executive_alter_lead_platform'),
    ]

    operations = [
        migrations.AddField(
            model_name='lead',
            name='is_verified',
            field=models.BooleanField(default=False),
        ),
    ]
