# Generated by Django 4.2 on 2024-12-30 16:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Store', '0005_alter_order_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reviewrating',
            name='status',
            field=models.BooleanField(default=False, help_text='0=default , 1=Hidden'),
        ),
    ]
