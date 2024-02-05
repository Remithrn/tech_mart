from django.shortcuts import render, redirect
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
            message_handler = MessageHandler(request.POST['phone_number'], otp).send_otp_via_message()
            request.session['registration_data'] = {
                'first_name': form.cleaned_data['first_name'],
                'last_name': form.cleaned_data['last_name'],
                'address': form.cleaned_data['address'],
                'email': form.cleaned_data['email'],
                'phone_number': form.cleaned_data['phone_number'],
                'username': form.cleaned_data['username'],
                'password': form.cleaned_data['password1'],
                'otp': otp,
            }
            red = redirect('customer:otp')
            red.set_cookie("can_otp_enter", True, max_age=600)
            return red

        else:
            print(form.errors)
            messages.error(request, form.errors)

    return render(request, 'customer/register.html', {"form": form})

def verifyOtp(request):
    registration_data = request.session.get('registration_data', {})

    if not registration_data:
        return redirect('customer:register')

    first_name = registration_data.get('first_name', '')
    last_name = registration_data.get('last_name', '')
    address = registration_data.get('address', '')
    email = registration_data.get('email', '')
    phone_number = registration_data.get('phone_number', '')
    username = registration_data.get('username', '')
    password = registration_data.get('password', '')
    otp = registration_data.get('otp', '')

    if request.method == "POST":
        entered_otp = request.POST.get('otp')

        if str(otp) == entered_otp:
            if request.COOKIES.get('can_otp_enter') is None:
                print("Time is up")
                return redirect('customer:register')
            else:
                customer = Customer.objects.create(
                    first_name=first_name,
                    last_name=last_name,
                    address=address,
                    email=email,
                    phone_number=phone_number,
                    username=username
                )
                customer.set_password(password)
                customer.save()

                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request, user)
                    print("User created and logged in.")

                del request.session['registration_data']
                url = reverse('shop:home')
                return redirect(url)

        else:
            print("Wrong OTP")
            return redirect('customer:register')

    return render(request, 'customer/verify_otp.html', {'otp': otp})



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
