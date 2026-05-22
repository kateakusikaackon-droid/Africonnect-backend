from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL


class SupplierProfile(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="supplier_profile")
    business_name = models.CharField(max_length=255)

    verified = models.BooleanField(default=False)

    rating = models.DecimalField(max_digits=3,decimal_places=2,default=0.00)

    completion_rate = models.DecimalField(max_digits=5,decimal_places=2,default=0.00)
    
    gender = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    country = models.CharField(max_length=100)
    address = models.TextField(blank=True)
    website = models.URLField(blank=True)
    
    image = models.ImageField(upload_to="profiles/suppliers/", blank=True, null=True)

    is_public = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.email} Supplier_Profile"
    
    ##OR
    
    #def __str__(self):
        #return self.name
        
    ##OR
    
    #def __str__(self):
        #return self.business_name    