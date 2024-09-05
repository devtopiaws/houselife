# Generated by Django 4.2 on 2024-09-05 18:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0002_alter_product_category_alter_product_date_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='cod_supplier',
            field=models.CharField(max_length=100, null=True, verbose_name='Codigo Proveedor'),
        ),
        migrations.AddField(
            model_name='product',
            name='price_sell',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Precio Venta'),
        ),
        migrations.AddField(
            model_name='product',
            name='supplier',
            field=models.CharField(max_length=100, null=True, verbose_name='Nombre Proveedor'),
        ),
    ]
