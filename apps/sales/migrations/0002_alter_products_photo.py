# Generated by Django 4.2.11 on 2024-11-03 17:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("sales", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="products",
            name="photo",
            field=models.ImageField(null=True, upload_to="files/products/pictures/"),
        ),
    ]
