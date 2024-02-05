from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from .forms import RegisterUser,EditForm
from django.contrib import messages
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import user_passes_test
from django.views.decorators.cache import never_cache

# Create your views here.
def admin_view(request):
    qs = request.GET.get("qs")
    if qs:
        users=User.objects.filter(username__icontains=qs)
    else:
        users=User.objects.all()
    return render(request,'admin.html',{'users':users})

@user_passes_test(lambda u: u.is_superuser,login_url="error")
@never_cache
def user_detail_page(request,id):
    user=User.objects.get(id=id)
    return render(request,'detail.html',{'user':user})

@user_passes_test(lambda u: u.is_superuser,login_url="error")
@never_cache
def delete_user(request,id):
    user=User.objects.get(id=id)
    user.delete()
    return redirect('admin_view')


def edit_user(request,id):
    user=User.objects.get(id=id)
    form=EditForm(instance=user)
    if request.method=="POST":
        form=EditForm(request.POST,instance=user)
        if form.is_valid():
            form.save()
            messages.success(request,"user edited successfully")
            return redirect("admin_view")
        else:
            messages.error(request,form.errors)
            form=EditForm(instance=user)

            return render(request,'edit.html',{'form':form})
    return render(request,'edit.html',{'form':form})


def user_creation(request):
    form=RegisterUser()
    if request.method =="POST":
        form=RegisterUser(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"user created successfully!!")
            return redirect("login")
        else:
            messages.error(request,form.errors)
            return redirect("register")
    return render(request,"register.html",{'form':form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect("admin_view")
    if request.method=="POST":
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            messages.success(request,f"hello {username}")
            return redirect("admin_view")
        else:
            messages.error(request,"invalid credentials")        
            return redirect('login')
    return render(request,'login.html')


def logout_view(request):
    logout(request)
    messages.success(request,"logged out successfully!!")
    return redirect('login')

def error_view(request):
    messages.error(request,"only superusers are authorised for this function")
    return redirect("shop:admin_view")