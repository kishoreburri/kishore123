from django.contrib import admin
from .models import Brand, Product, ProductSpecification, Order, Feedback


# Register your models here.

admin.site.register(Brand)
admin.site.register(Product)
admin.site.register(ProductSpecification)
admin.site.register(Order)
admin.site.register(Feedback)


