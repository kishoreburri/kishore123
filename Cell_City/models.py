from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify



# Create your models here.

class Brand(models.Model):
    name = models.CharField(max_length=100)
    image_url = models.URLField()

    def __str__(self):
        return self.name

class Product(models.Model):
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    stock_quantity = models.PositiveIntegerField(default=0)
    image_url = models.URLField()
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return self.name
    

class ProductSpecification(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='specifications')
    name = models.CharField(max_length=100)
    value = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.name}: {self.value}'
    
class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.User.username
   
class Wishlist(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    products = models.ManyToManyField('Product')

    def __str__(self):
        return f"Wishlist for {self.user.username}"
    

class Address(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    street = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.street}, {self.city}, {self.state}, {self.country}"
    
from .utils import generate_order_id

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2)
    order_date = models.DateTimeField(auto_now_add=True)
    order_id = models.CharField(max_length=20, unique=True)
    


    def save(self, *args, **kwargs):
        if not self.order_id:
            self.order_id = generate_order_id()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Order #{self.order_id} - {self.user.username}"
    

from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    date_of_birth = models.DateField(blank=True, null=True)
    mobile_number = models.CharField(max_length=20, blank=True, null=True)

    class Meta(AbstractUser.Meta):
        pass

User._meta.get_field('groups').remote_field.related_name = 'user_custom_set'
User._meta.get_field('user_permissions').remote_field.related_name = 'user_custom_set'



