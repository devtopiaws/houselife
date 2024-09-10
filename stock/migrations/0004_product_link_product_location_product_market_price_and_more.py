# Generated by Django 4.2 on 2024-09-09 16:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0003_product_cod_supplier_product_price_sell_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='link',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='link'),
        ),
        migrations.AddField(
            model_name='product',
            name='location',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Ubicación'),
        ),
        migrations.AddField(
            model_name='product',
            name='market_price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Precio Venta'),
        ),
        migrations.AddField(
            model_name='product',
            name='subcategory',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Sub categoria'),
        ),
    ]
