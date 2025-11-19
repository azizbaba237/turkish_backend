from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class CategoryService(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class Color(models.Model):
    name = models.CharField(max_length=50)
    hex_code = models.CharField(max_length=7, blank=True, null=True)
    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=255)
    short_description = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    image = models.ImageField(upload_to='products/')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    colors = models.ManyToManyField(Color, blank=True)

    def __str__(self):
        return self.name

class Service(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.ForeignKey(CategoryService, on_delete=models.SET_NULL, null=True, blank=True)
    price = models.CharField(max_length=100, default="Sur devis")  
    features = models.JSONField(default=list, blank=True)  
    
    def __str__(self):
        return self.title
    
class ServiceImage(models.Model):
    service = models.ForeignKey(Service, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='services/')
    order = models.PositiveIntegerField(default=0)  # Pour ordonner les images
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return f"Image for {self.service.title}"

class Contact(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    message = models.TextField()
    phone = models.CharField(max_length=50, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.name} - {self.email}"

class Testimonials(models.Model):
    name = models.CharField(max_length=255)
    text = models.TextField()
    rating = models.PositiveIntegerField(default=5)
    
    def __str__(self):
        return f"{self.name} - {self.rating} stars"

# Newsletter
class NewsletterSubscriber(models.Model):
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email


