from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Product, Customer
from .forms import ProductForm, CustomerForm
from django.db.models import Q

# Vista para la página de inicio
def home(request):
    return render(request, 'pages/home.html')

# Vista para vista nosotros
def about(request):
    return render(request,'pages/about.html')

# Vista para clientes
def customer(request):
    customers = Customer.objects.all()
    return render(request, 'customers/index.html', {'customers': customers})


# Vista para crear un nuevo producto
def create_customer(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()  # Guarda el cliente
            return redirect('customer')  # Redirige a la lista de clientes u otra vista
    else:
        form = CustomerForm()
    
    return render(request, 'customers/create.html', {'form': form})

# Vista para editar un cliente existente
def edit_customer(request, id):
    customer = get_object_or_404(Customer, id=id)

    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            return redirect('customer')
    else:
        form = CustomerForm(instance=customer)

    return render(request, 'customers/edit.html', {'form': form, 'customer': customer})


# Vista para eliminar un cliente
def delete_customer(request, id):
    customer = get_object_or_404(Customer, id=id)
    customer.delete()
    return redirect('customer')

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
