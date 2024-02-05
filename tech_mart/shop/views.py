from django.shortcuts import render
from django.views.generic import ListView,DetailView
from .models import Product
# Create your views here.
class ProductList(ListView):
    model = Product
    context_object_name = 'products'
    template_name='shop/productlist.html'

class ProductDetail(DetailView):
    model = Product
    template_name='shop/productdetail.html'
    context_object_name = 'product'
    slug_url_kwarg='slug'
def home(request):
    return render(request,"base.html")