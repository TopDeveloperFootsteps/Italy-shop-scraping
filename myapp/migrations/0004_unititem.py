# Generated by Django 5.1.6 on 2025-03-06 13:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0003_productitem_unit'),
    ]

    operations = [
        migrations.CreateModel(
            name='UnitItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unit', models.CharField(max_length=100, unique=True)),
            ],
        ),
    ]
