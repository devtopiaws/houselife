from django import forms
from .models import Product, Customer, Supplier


class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = ['name', 'email', 'phone', 'address', 'city', 'country']

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['first_name', 'last_name', 'email', 'phone', 'address', 'city', 'country']

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
        widgets = {
            'date': forms.DateInput(format='%d/%m/%Y', attrs={'class': 'form-control', 'placeholder': 'DD/MM/YYYY'}),
        }
    
    # Aseguramos que Django acepte el formato de fecha correcto
    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        self.fields['date'].input_formats = ['%d/%m/%Y']


