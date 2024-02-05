from django.shortcuts import render,redirect,get_object_or_404
from .forms import AdminCreationForm,DeactivateCustomerForm
from django.contrib import messages
from shop.forms import ProductForm,CategoryForm
from customer.models import Customer
from shop.models import Product,Category
from django.contrib.auth.decorators import user_passes_test
from django.views.decorators.cache import never_cache

@never_cache
def adminRegistration(request):
    if request.user.is_authenticated:
        return redirect('customer:dashboard')
    form=AdminCreationForm()
    if request.method =="POST":
        form=AdminCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"admin user created successfully!!")
            return redirect("customer:login")
        else:
            messages.error(request,form.errors)
            return redirect("adminUser:adminregistration")
    return render(request,"adminUser/register.html",{'form':form})

@user_passes_test(lambda u: u.is_superuser,login_url="adminUser:error")
@never_cache
def adminDashboard(request):
    users=Customer.objects.all()
    products=Product.objects.all()
    categories=Category.objects.all()

    context={
        'users':users,
        'products':products,
        'categories':categories
    }

    return render(request,"adminUser/dashboard.html",context)
@user_passes_test(lambda u: u.is_superuser,login_url="adminUser:error")
@never_cache
def toggle_customer_status(request, customer_id):
    customer = get_object_or_404(Customer, id=customer_id)

    if request.method == 'POST':
        confirm_deactivation = request.POST.get('confirm_deactivation') == 'on'

        if customer.is_active and confirm_deactivation:
            # Deactivate the customer
            customer.is_active = False
            messages.success(request, f"{customer.username} deactivated successfully.")
        elif not customer.is_active:
            # Activate the customer
            customer.is_active = True
            messages.success(request, f"{customer.username} activated successfully.")
        else:
            messages.warning(request, "Invalid request. Please try again.")

        customer.save()

    return redirect('adminUser:dashboard')

@user_passes_test(lambda u: u.is_superuser,login_url="adminUser:error")
@never_cache
def create_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category created successfully.')
            return redirect('adminUser:dashboard')
        else:
            messages.error(request, form.errors)
    else:
        form = CategoryForm()

    return render(request, 'adminUser/create_new.html', {'form': form})
@user_passes_test(lambda u: u.is_superuser,login_url="error")
@never_cache
def create_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product created successfully.')
            return redirect('adminUser:dashboard')
        else:
            messages.error(request, form.errors)
    else:
        form = ProductForm()

    return render(request, 'adminUser/create_new.html', {'form': form})
@user_passes_test(lambda u: u.is_superuser,login_url="adminUser:error")
@never_cache
def edit_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    form=CategoryForm()
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request,"updated successfully")
            return redirect('adminUser:dashboard')
    else:
        form = CategoryForm(instance=category)
        messages.error(request,form.errors)


    return render(request, 'adminUser/edit.html', {'form': form, 'model': 'Category'})

@user_passes_test(lambda u: u.is_superuser,login_url="adminUser:error")
@never_cache
def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    form=ProductForm()
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request,"updated successfully")
            return redirect('adminUser:dashboard')
    else:
        messages.error(request,form.errors)
        form = ProductForm(instance=product)

    return render(request, 'adminUser/edit.html', {'form': form, 'model': 'Product'})
@user_passes_test(lambda u: u.is_superuser,login_url="adminUser:error")
@never_cache
def delete_category(request,category_id):
    category = get_object_or_404(Category, id=category_id)
    try:
        category.delete()
        messages.success(request, "Deleted category successfully.")
    except Exception as e:
        messages.error(request, f"Error deleting category: {e}")

    return redirect('adminUser:dashboard')
@user_passes_test(lambda u: u.is_superuser,login_url="error")
@never_cache
def delete_product(request,product_id):
    product = get_object_or_404(Product, id=product_id)
    try:
        product.delete()
        messages.success(request, "Deleted product successfully.")
    except Exception as e:
        messages.error(request, f"Error deleting product: {e}")
        

    return redirect('adminUser:dashboard')


def error_view(request):
    messages.error(request,"only admims are authorised for this function")
    return redirect("shop:home")



