from customer.models import Customer
from django.contrib.auth.forms import UserCreationForm
from django import forms

class AdminCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Customer
        fields = (
            "first_name",
            "last_name",
            "address",
            "email",
            "phone_number",
            "username",
            "is_superuser",
        )
    def save(self, commit=True):
        user = super().save(commit=False)

        if self.cleaned_data['is_superuser']:
            user.is_staff = True

        if commit:
            user.save()

        return user
    
class DeactivateCustomerForm(forms.Form):
    confirm_deactivation = forms.BooleanField(
        required=True,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )

