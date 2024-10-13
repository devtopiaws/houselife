
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
import json
from .models import Product, Customer, Supplier, MarketStudy
from .forms import ProductForm, CustomerForm, SupplierForm, MarketStudyForm
from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib.auth import login
from .forms import SignUpForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from .integrations.woocommerce import obtener_productos, actualizar_inventario_producto, actualizar_inventario_en_woocommerce
from .models import Product  # Importa el modelo Product de Django



class VistaProtegida(LoginRequiredMixin, TemplateView):
    template_name = 'login.html'


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Loguea al usuario automáticamente tras el registro
            return redirect('/')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


# Vista para la página de inicio

def home(request):
    return render(request, 'pages/home.html')

# Vista para vista nosotros
def about(request):
    return render(request,'pages/about.html')

@login_required
def edit(request, id):
    product = Product.objects.get(id=id)
    formulary = ProductForm(request.POST or None, request.FILES or None, instance=product)
    if formulary.is_valid() and request.POST:
        producto_actualizado = formulary.save()
        # Llama a la función para actualizar el inventario en WooCommerce
        actualizar_inventario_producto(producto_actualizado.id, producto_actualizado.stock)
        return redirect('products')
    return render(request, 'products/edit.html', {'formulary': formulary})

def woocommerce_webhook(request):
    if request.method == 'POST':
        payload = json.loads(request.body)
        try:
            for item in payload['line_items']:
                product_id = item['product_id']
                quantity = item['quantity']

                # Busca el producto en tu aplicación Django basado en el ID de WooCommerce
                producto_local = Product.objects.filter(id=product_id).first()

                if producto_local:
                    # Resta la cantidad vendida del inventario local
                    producto_local.stock -= quantity
                    producto_local.save()

            return JsonResponse({'status': 'success'}, status=200)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    else:
        return JsonResponse({'status': 'method not allowed'}, status=405)

# Sincronizacion del invenario de house life con la app de inventario
@login_required
def sincronizar_inventario(request):
    try:
        productos_woocommerce = obtener_productos()
        # print(f"Productos obtenidos de WooCommerce: {productos_woocommerce}")

        productos_actualizados = []
        productos_con_stock_django = {}  # Diccionario para almacenar el stock de Django por nombre de producto

        if productos_woocommerce:
            for producto_wc in productos_woocommerce:
                nombre_producto_wc = producto_wc['name'].strip()
                stock_producto_wc = producto_wc['stock_quantity']
                # print(f"Producto en WooCommerce: {nombre_producto_wc}, Stock: {stock_producto_wc}")

                # Busca el producto en Django por nombre exacto (ignora mayúsculas/minúsculas)
                producto_django = Product.objects.filter(name__iexact=nombre_producto_wc).first()

                if producto_django:
                    # print(f"Producto encontrado en Django: {producto_django.name}, Stock: {producto_django.stock}")
                    productos_con_stock_django[producto_wc['name']] = producto_django.stock  # Asigna el stock de Django
                    if producto_django.stock != stock_producto_wc:
                        producto_django.stock = stock_producto_wc
                        producto_django.save()
                        productos_actualizados.append(producto_django)
                        print(f"Producto {producto_django.name} actualizado en Django")
                else:
                    # print(f"Producto {nombre_producto_wc} no encontrado en la base de datos de Django")
                    pass

        else:
            print("No se encontraron productos en WooCommerce.")
            productos_woocommerce = []

    except Exception as e:
        print(f"Error al sincronizar el inventario: {e}")
        productos_woocommerce = []

    # Paginación de productos (10 productos por página)
    paginator = Paginator(productos_woocommerce, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'woocommerce/sincronizar_inventario.html', {
        'page_obj': page_obj,
        'productos_actualizados': productos_actualizados,
        'productos_con_stock_django': productos_con_stock_django  # Pasamos el diccionario de stock de Django
    })


# Listado de estudios de mercado con búsqueda y paginación
@login_required
def study(request):
    query = request.GET.get('q', '')
    if query:
        studies = MarketStudy.objects.filter(product__name__icontains=query)
    else:
        studies = MarketStudy.objects.all() 


    # Agregar paginación
    paginator = Paginator(studies, 10)  # 10 estudios de mercado por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'studies/index.html', {'page_obj': page_obj, 'query': query})

# Crear un nuevo estudio de mercado
@login_required
def create_study(request):
    if request.method == 'POST':
        form = MarketStudyForm(request.POST)
        if form.is_valid():
            # Guardar el estudio de mercado
            study = form.save(commit=False)
            # Aquí puedes agregar lógica adicional antes de guardar, como cálculos de IVA o transporte
            study.save()
            return redirect('study')
    else:
        form = MarketStudyForm()
    
    return render(request, 'studies/create.html', {'form': form})

# Editar un estudio de mercado existente
@login_required
def edit_study(request, id):
    study = get_object_or_404(MarketStudy, id=id)

    if request.method == 'POST':
        form = MarketStudyForm(request.POST, instance=study)
        if form.is_valid():
            form.save()
            return redirect('study')
    else:
        form = MarketStudyForm(instance=study)

    return render(request, 'studies/edit.html', {'form': form, 'study': study})

# Eliminar un estudio de mercado
@login_required
def delete_study(request, id):
    study = get_object_or_404(MarketStudy, id=id)
    study.delete()
    return redirect('study')


# Vista para Proveedores
@login_required
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
@login_required
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
@login_required
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
@login_required
def delete_supplier(request, id):
    supplier = get_object_or_404(Supplier, id=id)
    supplier.delete()
    return redirect('supplier')




# Vista para clientes
@login_required
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
@login_required
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
@login_required
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
@login_required
def delete_customer(request, id):
    customer = get_object_or_404(Customer, id=id)
    customer.delete()
    return redirect('customer')

# Vista para listar todos los productos con filtro de búsqueda y paginación
@login_required
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
@login_required
def create(request):
    formulary = ProductForm(request.POST or None, request.FILES or None)
    if formulary.is_valid():
        formulary.save()
        return redirect('products')
    return render(request, 'products/create.html', {'formulary': formulary})

# Vista para editar un producto existente
@login_required
def edit(request, id):
    product = Product.objects.get(id=id)
    formulary = ProductForm(request.POST or None, request.FILES or None, instance=product)
    if formulary.is_valid() and request.POST:
        formulary.save()
        return redirect('products')
    return render(request, 'products/edit.html', {'formulary': formulary})

# Vista para eliminar un producto
@login_required
def delete(request, id):
    product = Product.objects.get(id=id)
    product.delete()
    return redirect('products')
