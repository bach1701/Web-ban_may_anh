# Generated by Django 5.0.6 on 2024-05-24 11:19

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("app", "0004_remove_product_companyproduct_product_category"),
    ]

    operations = [
        migrations.AddField(
            model_name="product",
            name="detail",
            field=models.TextField(blank=True, null=True),
        ),
    ]