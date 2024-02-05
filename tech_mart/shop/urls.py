from django.urls import path
from . import views
app_name="shop"

urlpatterns=[
   
    path("",views.ProductList.as_view(),name="home"),
    path("product/<str:slug>",views.ProductDetail.as_view(),name="detail")
]