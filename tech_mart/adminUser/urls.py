from django.urls import path
from . import views
app_name='adminUser'
urlpatterns=[
    path("",views.adminDashboard,name='dashboard'),
    path("register",views.adminRegistration,name='adminregistration'),
    path('toggle/customer/<int:customer_id>/', views.toggle_customer_status, name='toggle_customer_status'),
    path('create/category/', views.create_category, name='create_category'),
    path('create/product/', views.create_product, name='create_product'),
    path('edit/category/<int:category_id>/', views.edit_category, name='edit_category'),
    path('delete/category/<int:category_id>/', views.delete_category, name='delete_category'),
    path('edit/product/<int:product_id>/', views.edit_product, name='edit_product'),
    path('delete/product/<int:product_id>/', views.delete_product, name='delete_product'),
    path('error/',views.error_view,name='error'),
]