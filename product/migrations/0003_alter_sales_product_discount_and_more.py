# Generated by Django 4.2.7 on 2023-12-02 12:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0002_alter_sales_product_bill_no_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sales_product',
            name='discount',
            field=models.CharField(max_length=9),
        ),
        migrations.AlterField(
            model_name='sales_product',
            name='sale_product_datetime',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
