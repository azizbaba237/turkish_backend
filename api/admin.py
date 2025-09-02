from django.contrib import admin
from django.contrib.admin import site
from .models import Category, Color, Product, Service, Contact, CategoryService, ServiceImage, Testimonials


class ServiceImageInline(admin.TabularInline):  # ou admin.StackedInline
    model = ServiceImage
    extra = 3  # nombre de champs image par défaut

class ServiceAdmin(admin.ModelAdmin):
    inlines = [ServiceImageInline]
    
# Register your models here.
admin.site.register(Category)
admin.site.register(Color)
admin.site.register(Product)
admin.site.register(Service, ServiceAdmin)
admin.site.register(Contact)
admin.site.register(CategoryService)
admin.site.register(ServiceImage)
admin.site.register(Testimonials)