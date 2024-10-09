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
    """Obtiene la lista de productos de WooCommerce."""
    response = wcapi.get("products")
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error al obtener productos: {response.status_code}")
        return None

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
