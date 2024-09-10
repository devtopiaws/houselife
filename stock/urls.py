from django.urls import path
from . import views


from django.conf import settings
from django.contrib.staticfiles.urls import static

urlpatterns = [
    path('', views.home, name="home"),
    path('home', views.home, name="home"),
    path('about', views.about, name="about"),
    path('products', views.products, name="products"),
    path('products/create', views.create, name="create"),
    path('products/edit', views.edit, name="edit"),
    path('delete/<int:id>', views.delete, name="delete"),
    path('edit/<int:id>', views.edit, name="edit"),
    path('customers/', views.customer, name='customer'),  # Aquí está el nombre 'customer'
    path('customers/create/', views.create_customer, name='create_customer'),
    path('customers/edit/<int:id>/', views.edit_customer, name='edit_customer'),

    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)