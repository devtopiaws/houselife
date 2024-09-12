from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Product, Customer, Supplier
from .forms import ProductForm, CustomerForm, SupplierForm
from django.db.models import Q
from django.core.paginator import Paginator

# Vista para la página de inicio
def home(request):
    return render(request, 'pages/home.html')

# Vista para vista nosotros
def about(request):
    return render(request,'pages/about.html')

# Vista para Proveedores
def supplier(request):
    query = request.GET.get('q')
    if query:
        suppliers = Supplier.objects.filter(
            Q(name__icontains=query) | 
            Q(address__icontains=query) |
            Q(city__icontains=query) |
            Q(country__icontains=query) |
            Q(phone__icontains=query) |
            Q(email__icontains=query)  # Sin coma al final
        )
    else:
        suppliers = Supplier.objects.all()

    # Agregar paginación
    paginator = Paginator(suppliers, 10)  # 10 proveedores por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'suppliers/index.html', {'page_obj': page_obj, 'query': query})



# Vista para crear un nuevo producto
def create_supplier(request):
    if request.method == 'POST':
        form = SupplierForm(request.POST)
        if form.is_valid():
            form.save()  # Guarda el proveedor
            return redirect('supplier')  # Redirige a la lista de proveedor u otra vista
    else:
        form = SupplierForm()
    
    return render(request, 'suppliers/create.html', {'form': form})

# Vista para editar un proveedor existente
def edit_supplier(request, id):
    supplier = get_object_or_404(Supplier, id=id)

    if request.method == 'POST':
        form = SupplierForm(request.POST, instance=supplier)
        if form.is_valid():
            form.save()
            return redirect('supplier')
    else:
        form = SupplierForm(instance=supplier)

    return render(request, 'suppliers/edit.html', {'form': form, 'supplier': supplier})


# Vista para eliminar un proveedor
def delete_supplier(request, id):
    supplier = get_object_or_404(Supplier, id=id)
    supplier.delete()
    return redirect('supplier')















# Vista para clientes
def customer(request):
    query = request.GET.get('q')
    if query:
        customers = Customer.objects.filter(
            Q(first_name__icontains=query) | 
            Q(last_name__icontains=query) |
            Q(email__icontains=query) |
            Q(phone__icontains=query) |
            Q(address__icontains=query) |
            Q(city__icontains=query) |
            Q(country__icontains=query) |
            Q(date_created__icontains=query)
        )
    else:
        customers = Customer.objects.all()

    # Agregar paginación
    paginator = Paginator(customers, 10)  # 5 clientes por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'customers/index.html', {'page_obj': page_obj, 'query': query})


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

# Vista para listar todos los productos con filtro de búsqueda y paginación
def products(request):
    query = request.GET.get('q')
    if query:
        products = Product.objects.filter(
            Q(name__icontains=query) | 
            Q(description__icontains=query) |
            Q(price__icontains=query) |
            Q(price_sell__icontains=query) |
            Q(market_price__icontains=query) |
            Q(cod_supplier__icontains=query) |
            Q(supplier__icontains=query) |
            Q(stock__icontains=query) |
            Q(category__icontains=query)
        )
    else:
        products = Product.objects.all()
    
    # Agregar paginación
    paginator = Paginator(products, 10)  # 10 productos por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'products/index.html', {'page_obj': page_obj, 'query': query})

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
