from django.shortcuts import render, redirect,get_object_or_404
from django.urls import reverse
from .models import Customer
from .forms import CustomerRegistrationForm
import random
from .helper import MessageHandler
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

# Create your views here.

def registerView(request):
    form = CustomerRegistrationForm()

    if request.method == "POST":
        form = CustomerRegistrationForm(request.POST)
             
        if form.is_valid():
            messages.success(request, "Registration successful!")
            otp = random.randint(1000, 9999)
           
            customer=form.save(commit=False)
            customer.otp=otp
            customer.save()
            print(customer.id)
            red=redirect('customer:otp',customer.id)
            red.set_cookie("can_otp_enter",True,max_age=600)
            return red

        else:
            print(form.errors)
            messages.error(request, form.errors)

    return render(request, 'customer/register.html', {"form": form})

def verifyOtp(request,id):
    # customer = get_object_or_404(Customer, id=id)
    if request.method=="POST":
        profile=Customer.objects.get(id=id)     
        if request.COOKIES.get('can_otp_enter')!=None:
            if(profile.otp==request.POST['otp']):
                profile.is_verified=True
                profile.save()
                red=redirect("shop:home")
                red.set_cookie('verified',True)
                return red
            messages.error(request,"wrong OTP")
            return render(request,"customer/verify_otp.html",{'id':id})
        messages.error(request,"wrong OTP")
        return render(request,"customer/verify_otp.html",{'id':id})        
    return render(request,"customer/verify_otp.html",{'id':id})

    



def logout_view(request):
    logout(request)
    return redirect('shop:home')

def login_view(request):
    if request.user.is_authenticated:
        return redirect("shop:home")
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f"Hello {username}")
            return redirect("shop:home")
        else:
            messages.error(request, "Invalid credentials")
            return redirect('customer:login')

    return render(request, 'customer/login.html')
