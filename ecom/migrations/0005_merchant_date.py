# Generated by Django 3.0.5 on 2020-08-29 12:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecom', '0004_feedback'),
    ]

    operations = [
      migrations.CreateModel(
            name='Merchant',
            fields=[
                ('KEY', models.CharField(max_length=40)),
                ('VALUE', models.CharField(max_length=40)),

            ],
        ),
    ]
