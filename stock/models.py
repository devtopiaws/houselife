from django.db import models

# Create your models here.
class Product(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, verbose_name='Nombre')
    description = models.TextField(verbose_name='Descripción', null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Precio', null=True, blank=True)
    stock = models.PositiveIntegerField(verbose_name='Stock', null=True, blank=True)
    category = models.CharField(max_length=100, verbose_name='Categoría', null=True, blank=True)
    image = models.ImageField(upload_to='images/', verbose_name='Imagen', null=True, blank=True)
    date = models.DateField(verbose_name='Fecha', null=True, blank=True)
    

                    
    def __str__(self):
        fila = "Nombre: "+ self.name + " - " + "Descripción:" + self.description
        return fila

    def delete(self, using=None, keep_parent=False):
        self.image.delete(self.image.name)
        super().delete()