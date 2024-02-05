from django.urls import path
from . import views
app_name='customer'
urlpatterns=[
    path('',views.registerView,name='register'),
    path('otp/', views.verifyOtp, name='otp'),
    
    path("login/",views.login_view,name='login'),
    path("logout/",views.logout_view,name='logout')
]