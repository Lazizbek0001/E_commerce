from django.db import models
from django.contrib.auth.models import User


class ShippingAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    full_name = models.CharField(max_length=255)
    email = models.CharField(max_length=200)
    address1 = models.CharField(max_length=200)
    address2 = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    state = models.CharField(max_length=200, null=True,blank=True)
    zipcode = models.CharField(max_length=200,null=True,blank=True)
    country = models.CharField(max_length=200)

    class Meta:
        verbose_name_plural = "Shipping Address"
        
    def __str__(self) -> str:
        return f"Shipping Address - {str(self.id)}"