from django.urls import path
from . import views
urlpatterns=[
    path('',views.admin_view,name='admin_view'),
    path('detail/<int:id>',views.user_detail_page,name='detail'),
    path('delete/<int:id>',views.delete_user,name='delete'),
    path('register',views.user_creation,name='register'),
    path('login/',views.login_view,name="login"),
    path('logout/',views.logout_view,name='logout'),
    path('error/',views.error_view,name='error'),
    path('edit/<int:id>',views.edit_user,name='edit_user')
    
    
   
]