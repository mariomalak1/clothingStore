# Generated by Django 4.2 on 2023-04-17 16:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("Invoice", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="cart",
            name="cart_code",
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
