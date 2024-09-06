from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Product
from .forms import ProductForm  
from django.db.models import Q

# Vista para la página de inicio
def home(request):
    return render(request, 'pages/home.html')

# Vista para vista nosotros
def about(request):
    return render(request,'pages/about.html')

# Vista para listar todos los productos con filtro de búsqueda
def products(request):
    query = request.GET.get('q')
    if query:
        products = Product.objects.filter(
            Q(name__icontains=query) | 
            Q(description__icontains=query) |
            Q(price__icontains=query) |
            Q(price_sell__icontains=query) |
            Q(cod_supplier__icontains=query) |
            Q(supplier__icontains=query) |
            Q(stock__icontains=query) |
            Q(category__icontains=query)
        )
    else:
        products = Product.objects.all()
    return render(request, 'products/index.html', {'products': products})

# Vista para crear un nuevo producto
def create(request):
    formulary = ProductForm(request.POST or None, request.FILES or None)
    if formulary.is_valid():
        formulary.save()
        return redirect('products')
    return render(request, 'products/create.html', {'formulary': formulary})

# Vista para editar un producto existente
def edit(request, id):
    product = Product.objects.get(id=id)
    formulary = ProductForm(request.POST or None, request.FILES or None, instance=product)
    if formulary.is_valid() and request.POST:
        formulary.save()
        return redirect('products')
    return render(request, 'products/edit.html', {'formulary': formulary})

# Vista para eliminar un producto
def delete(request, id):
    product = Product.objects.get(id=id)
    product.delete()
    return redirect('products')
