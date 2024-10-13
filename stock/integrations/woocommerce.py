from woocommerce import API
import os

# Configura la conexión con WooCommerce usando las claves de consumidor y la URL del sitio
wcapi = API(
    url="https://houselife.com.co/",  # Cambia esto por la URL de tu tienda WooCommerce
    consumer_key=os.getenv("WC_CONSUMER_KEY"),  # Lee las claves desde las variables de entorno
    consumer_secret=os.getenv("WC_CONSUMER_SECRET"),
    version="wc/v3"
)

def obtener_productos():
    """Obtiene todos los productos de WooCommerce, manejando la paginación."""
    productos = []
    page = 1

    while True:
        # Solicita una página de productos (con un límite de 100 productos por página)
        response = wcapi.get("products", params={"per_page": 100, "page": page})
        if response.status_code == 200:
            productos_pagina = response.json()

            if not productos_pagina:
                break  # Si no hay más productos, salimos del bucle

            productos.extend(productos_pagina)  # Agrega los productos a la lista general
            page += 1  # Pasa a la siguiente página
        else:
            print(f"Error al obtener productos de WooCommerce: {response.status_code}")
            break

    return productos

def actualizar_inventario_producto(product_id, cantidad):
    """Actualiza el inventario de un producto en WooCommerce."""
    data = {
        "stock_quantity": cantidad
    }
    response = wcapi.put(f"products/{product_id}", data)
    if response.status_code == 200:
        print(f"Inventario actualizado para el producto {product_id}")
    else:
        print(f"Error al actualizar inventario: {response.status_code} - {response.text}")

def actualizar_inventario_en_woocommerce(product_id, cantidad):
    """Actualiza el inventario de un producto en WooCommerce."""
    data = {
        "stock_quantity": cantidad
    }
    response = wcapi.put(f"products/{product_id}", data)
    if response.status_code == 200:
        print(f"Inventario actualizado para el producto {product_id} en WooCommerce.")
    else:
        print(f"Error al actualizar inventario en WooCommerce: {response.status_code} - {response.text}")