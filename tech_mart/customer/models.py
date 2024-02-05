from django.db import models
from django.contrib.auth.models import AbstractUser
# Created Customer 

class Customer(AbstractUser):
    phone_number=models.CharField(max_length=15)
    address=models.TextField()

    groups = models.ManyToManyField(
        "auth.Group",
        related_name="customer_groups",
        related_query_name="customer_group",
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="customer_user_permissions",
        related_query_name="customer_user_permission",
        blank=True,
    )