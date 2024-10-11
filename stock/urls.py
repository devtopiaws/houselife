from django.urls import path
from . import views


from django.conf import settings
from django.contrib.staticfiles.urls import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', views.signup, name='signup'),
    path('', views.home, name="home"),
    path('home', views.home, name="home"),
    path('about', views.about, name="about"),
    path('products', views.products, name="products"),
    path('products/create', views.create, name="create"),
    path('products/edit', views.edit, name="edit"),
    path('delete/<int:id>', views.delete, name="delete"),
    path('edit/<int:id>', views.edit, name="edit"),
    path('customers/', views.customer, name='customer'),  
    path('customers/create/', views.create_customer, name='create_customer'),
    path('customers/edit/<int:id>/', views.edit_customer, name='edit_customer'),
    path('customers/delete/<int:id>/', views.delete_customer, name='delete_customer'),
    path('suppliers/', views.supplier, name='supplier'),
    path('suppliers/create/', views.create_supplier, name='create_supplier'),
    path('suppliers/edit/<int:id>/', views.edit_supplier, name='edit_supplier'),
    path('suppliers/delete/<int:id>/', views.delete_supplier, name='delete_supplier'),
    path('studies/', views.study, name='study'),  
    path('studies/create/', views.create_study, name='create_study'),
    path('studies/<int:id>/edit/', views.edit_study, name='edit_study'),
    path('studies/<int:id>/delete/', views.delete_study, name='delete_study'),
    path('sincronizar_inventario/', views.sincronizar_inventario, name='sincronizar_inventario'),
    path('webhook/woocommerce/', views.woocommerce_webhook, name='woocommerce_webhook'),
    

    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)