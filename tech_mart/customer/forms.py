from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Customer

# Customer registration form

class CustomerRegistrationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Customer
        fields = (
            "first_name",
            "last_name",
            "address",
            "email",
            "phone_number",
            "username",
        )
