# Generated by Django 4.1.5 on 2023-04-20 11:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("Invoice", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="cart",
            name="created_at",
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]
