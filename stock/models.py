from django.db import models

# Create your models here.
class Customer(models.Model):
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=100, verbose_name='Nombre')
    last_name = models.CharField(max_length=100, verbose_name='Apellido')
    email = models.EmailField(unique=True, verbose_name='Correo Electrónico')
    phone = models.CharField(max_length=15, verbose_name='Teléfono', null=True, blank=True)
    address = models.TextField(verbose_name='Dirección', null=True, blank=True)
    city = models.CharField(max_length=100, verbose_name='Ciudad', null=True, blank=True)
    country = models.CharField(max_length=100, verbose_name='País', null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Registro')

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.email}"

class Product(models.Model):
    id = models.AutoField(primary_key=True)
    cod_supplier = models.CharField(max_length=100, verbose_name='Codigo Proveedor', null=True)
    supplier = models.CharField(max_length=100, verbose_name='Nombre Proveedor', null=True)
    name = models.CharField(max_length=100, verbose_name='Nombre')
    description = models.TextField(verbose_name='Descripción', null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Precio', null=True, blank=True)
    price_sell = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Precio Venta', null=True, blank=True)
    market_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Precio Mercado', null=True, blank=True)
    link = models.CharField(max_length=500, verbose_name='link', null=True, blank=True)
    stock = models.PositiveIntegerField(verbose_name='Stock', null=True, blank=True)
    category = models.CharField(max_length=100, verbose_name='Categoría', null=True, blank=True)
    subcategory = models.CharField(max_length=100, verbose_name='Sub categoria' , null=True, blank=True)
    image = models.ImageField(upload_to='images/', verbose_name='Imagen', null=True, blank=True)
    date = models.DateField(verbose_name='Fecha', null=True, blank=True)
    location = models.CharField(max_length=100, verbose_name='Ubicación',null=True, blank=True)
                    
    def __str__(self):
        fila = "Nombre: "+ self.name + " - " + "Descripción:" + self.description
        return fila

    def delete(self, using=None, keep_parent=False):
        self.image.delete(self.image.name)
        super().delete()