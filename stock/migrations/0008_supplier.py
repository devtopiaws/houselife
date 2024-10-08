# Generated by Django 4.2 on 2024-09-12 04:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0007_customer'),
    ]

    operations = [
        migrations.CreateModel(
            name='Supplier',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100, verbose_name='Nombre')),
                ('address', models.TextField(blank=True, null=True, verbose_name='Dirección')),
                ('city', models.CharField(blank=True, max_length=100, null=True, verbose_name='Ciudad')),
                ('country', models.CharField(blank=True, max_length=100, null=True, verbose_name='País')),
                ('phone', models.CharField(blank=True, max_length=15, null=True, verbose_name='Teléfono')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='Correo Electrónico')),
            ],
        ),
    ]
