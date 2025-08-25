from django.contrib import admin
from django.contrib.admin import site
from .models import Category, Color, Product, Service, Contact

# Register your models here.
site.register(Category)
site.register(Color)
site.register(Product)
site.register(Service)
site.register(Contact)