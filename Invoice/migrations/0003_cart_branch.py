# Generated by Django 4.2 on 2023-06-27 01:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("Seller", "0002_alter_site_user_branch"),
        ("Invoice", "0002_alter_cart_buyer_alter_cart_created_by"),
    ]

    operations = [
        migrations.AddField(
            model_name="cart",
            name="branch",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="Seller.branch",
            ),
        ),
    ]
